from pprint import pprint
from rest_framework import serializers

from management.models import Order, OrderDetail, OrderRefund, OrderRefundDetail, Promotion, PromotionDetail, PromotionHistory, PromotionLine, WarehouseTransaction
from management.serializers.product import PriceDetailSerializer, ReadProductSerializer, UnitExchangeSerializer
from management.serializers.user import CustomerSerializer, UserSerializer

class OrderDetailSerializer(serializers.ModelSerializer):
    promotion_line = serializers.IntegerField(allow_null=True)
    class Meta:
        model = OrderDetail
        exclude = ('order', )
        read_only_fields = ('total', 'price')


class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    promotion = serializers.IntegerField(allow_null=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total', 'final_total', 'date_created', 
            'user_created', 'date_updated', 'user_updated')
        # extra_kwargs = {
        #     "customer": {
        #         "required": False
        #     }
        # }

    def create(self, validated_data):
        details = validated_data.pop('details')
        promotion_order = validated_data.pop('promotion') if "promotion" in validated_data.keys() else None
        if promotion_order:
            promotion_order = PromotionLine.objects.get(pk=promotion_order)
        obj = super().create(validated_data)
        total = 0
        for detail in details:
            quantity_base_unit = detail["quantity"]*detail["unit_exchange"].value
            detail["order"] = obj
            promotion_line = detail.pop('promotion_line') if "promotion_line" in detail.keys() else None

            detail["price"] = detail["product"].get_price_detail(detail["unit_exchange"])
            detail["total"] = detail["quantity"]*detail["price"].price
            detail = OrderDetail.objects.create(**detail)
            total += detail.total
            WarehouseTransaction.objects.create(
                product=detail.product,
                reference=detail.pk,
                change=-detail.get_quantity_dvtcb(),
                type="order"
            )
            # promotion product
            if promotion_line != None:
                promotion_line = PromotionLine.objects.get(pk = promotion_line)
                pl = promotion_line
                benefit_product = pl.benefit_product(
                    detail.product,
                    quantity_base_unit,
                    obj.customer
                )
                quantity_base_actual_received = pl.quantity_base_actual_received(
                    detail.product,
                    quantity_base_unit,
                    obj.customer
                )
                # print("promotion product #######################")
                # pprint(vars(detail))
                # pprint(vars(pl))
                # print(benefit_product, quantity_base_actual_received)
                if quantity_base_actual_received > 0:
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
                    PromotionHistory.objects.create(
                        promotion_line=promotion_line,
                        type="Product",
                        order=obj,
                        buy_order_detail=detail,
                        received_order_detail=detail_voucher,
                        quantity=quantity_base_actual_received//promotion_line.detail.quantity_received,
                        amount=benefit_product,
                        note=promotion_line.title
                    )
        final_total = total
        if promotion_order != None:
            benefit = promotion_order.benefit_order(total)
            final_total -= benefit
            PromotionHistory.objects.create(
                promotion_line=promotion_order,
                type="Order",
                order=obj,
                quantity=1,
                amount=benefit,
                note=promotion_order.title
            )

        obj.total = total
        obj.final_total = final_total
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
    customer = CustomerSerializer()
    user_created = UserSerializer()
    user_updated = UserSerializer()
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
                product=detail.product,
                reference=detail.pk,
                change=+detail.get_quantity_dvtcb(),
                type="refund"
            )
        obj.order.status = "cancel"
        obj.order.save()
        return obj
        
    # def update(self, instance, validated_data):
    #     details = validated_data.pop('details')
    #     # instance = super().update(instance, validated_data)
    #     instance.note = validated_data["note"] if "note" in validated_data else instance.note
    #     if (instance.status == "complete" and validated_data["status"] != "pending"):
    #         instance.status = validated_data["status"] if "status" in validated_data else instance.status
    #     instance.save()
    #     return instance

########
class ResponseOrderRefundDetailSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True)
    unit_exchange = UnitExchangeSerializer(read_only=True)
    class Meta:
        model = OrderRefundDetail
        fields = '__all__'

class ResponseOrderRefundSerializer(serializers.ModelSerializer):
    details = ResponseOrderRefundDetailSerializer(many=True)
    customer = CustomerSerializer(source="order.customer")
    user_created = UserSerializer()
    user_updated = UserSerializer()
    class Meta:
        model = OrderRefund
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
