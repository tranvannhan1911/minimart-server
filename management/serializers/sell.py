from rest_framework import serializers

from management.models import Order, OrderDetail, OrderRefund, OrderRefundDetail, Promotion, PromotionDetail, PromotionHistory, PromotionLine, WarehouseTransaction
from management.serializers.product import PriceDetailSerializer, ReadProductSerializer, UnitExchangeSerializer

class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        exclude = ('order', )
        read_only_fields = ('total', )


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

    def create(self, validated_data):
        details = validated_data.pop('details')
        obj = super().create(validated_data)
        total = 0
        for detail in details:
            quantity_base_unit = detail["quantity"]*detail["unit_exchange"].value
            detail["order"] = obj
            promotion_lines = PromotionLine.get_by_product(detail["product"])
            promotion_lines = PromotionLine.filter_customer(promotion_lines, obj.customer)
            promotion_line, benefit = PromotionLine.get_best_benefit_product(
                promotion_lines,
                detail["product"],
                quantity_base_unit,
                obj.customer
            )
            print("3", promotion_line)
            if promotion_line != None:
                pl = promotion_line
                quantity_base_actual_received = pl.quantity_base_actual_received(
                    detail["product"],
                    quantity_base_unit,
                    obj.customer
                )
                detail_voucher = {
                    "order": obj,
                    "quantity": quantity_base_actual_received,
                    "unit_exchange": pl.detail.product_received.get_unit_exchange(),
                    "product": pl.detail.product_received,
                    "price": None
                }
                detail_voucher = OrderDetail.objects.create(**detail_voucher)
                WarehouseTransaction.objects.create(
                    product=detail_voucher.product,
                    reference=detail_voucher.pk,
                    change=-quantity_base_actual_received,
                    type="promotion"
                )

            detail["total"] = detail["quantity"]*detail["price"].price
            detail = OrderDetail.objects.create(**detail)
            total += detail.total
            WarehouseTransaction.objects.create(
                product=detail.product,
                reference=detail.pk,
                change=-detail.get_quantity_dvtcb(),
                type="order"
            )
            if promotion_line != None:
                PromotionHistory.objects.create(
                    promotion_line=promotion_line,
                    type="Product",
                    order=obj,
                    buy_order_detail=detail,
                    received_order_detail=detail_voucher,
                    quantity=quantity_base_actual_received//promotion_line.detail.quantity_received,
                    amount=benefit,
                    note=promotion_line.title
                )
        obj.total = total
        obj.save()
        return obj
        
    def update(self, instance, validated_data):
        details = validated_data.pop('details')

        instance.note = validated_data["note"] if "note" in validated_data else instance.note
        if instance.status == "pending" or (instance.status == "complete" and validated_data["status"] != "pending"):
            instance.status = validated_data["status"] if "status" in validated_data else instance.status
        instance.save()
        return instance

class ResponseOrderDetailSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True)
    unit_exchange = UnitExchangeSerializer(read_only=True)
    price = PriceDetailSerializer()
    class Meta:
        model = OrderDetail
        fields = '__all__'

class ResponseOrderSerializer(serializers.ModelSerializer):
    details = ResponseOrderDetailSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

######################

class OrderRefundDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRefundDetail
        exclude = ('order_refund', )
        read_only_fields = ('total', )


class OrderRefundSerializer(serializers.ModelSerializer):
    details = OrderRefundDetailSerializer(many=True)
    class Meta:
        model = OrderRefund
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

    def create(self, validated_data):
        details = validated_data.pop('details')
        obj = super().create(validated_data)
        for detail in details:
            detail["order_refund"] = obj
            detail = OrderRefundDetail.objects.create(**detail)
            
            WarehouseTransaction.objects.create(
                product=detail["product"],
                reference=detail.pk,
                change=+detail.get_quantity_dvtcb(),
                type="refund"
            )
        return obj
        
    def update(self, instance, validated_data):
        details = validated_data.pop('details')
        # instance = super().update(instance, validated_data)
        instance.note = validated_data["note"] if "note" in validated_data else instance.note
        if instance.status == "pending" or (instance.status == "complete" and validated_data["status"] != "pending"):
            instance.status = validated_data["status"] if "status" in validated_data else instance.status
        instance.save()
        return instance

########
class ResponseOrderRefundDetailSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True)
    unit_exchange = UnitExchangeSerializer(read_only=True)
    class Meta:
        model = OrderRefundDetail
        fields = '__all__'

class ResponseOrderRefundSerializer(serializers.ModelSerializer):
    details = ResponseOrderRefundDetailSerializer(many=True)
    class Meta:
        model = OrderRefund
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
