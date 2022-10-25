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
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
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

    def get_quantity_in_use_by_product(self, details, product_id):
        cnt = 0
        for detail in details:
            print("get_quantity_in_use_by_product", detail["product"], product_id)
            if detail["product"].id == product_id:
                quantity_base_unit = detail["quantity"]*detail["unit_exchange"].value
                cnt += quantity_base_unit
        return cnt


    def create(self, validated_data):
        details = validated_data.pop('details')
        promotion_order = validated_data.pop('promotion') if "promotion" in validated_data.keys() else None
        if promotion_order:
            promotion_order = PromotionLine.objects.get(pk=promotion_order)
        obj = super().create(validated_data)
        total = 0

        check = {}
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
            if detail.product.id not in check.keys() and promotion_line != None:
                quantity_inuse = self.get_quantity_in_use_by_product(details, detail.product.id)
                print("quantity_inuse", quantity_inuse)
                promotion_line = PromotionLine.objects.get(pk = promotion_line)
                pl = promotion_line
                benefit_product = pl.benefit_product(
                    detail.product,
                    quantity_inuse,
                    obj.customer
                )
                quantity_base_actual_received = pl.quantity_base_actual_received(
                    detail.product,
                    quantity_inuse,
                    obj.customer
                )
                # print("promotion product #######################")
                # pprint(vars(detail))
                # pprint(vars(pl))
                # print(benefit_product, quantity_base_actual_received)
                if quantity_base_actual_received > 0:
                    check[detail.product.id] = True
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
        
    # def update(self, instance, validated_data):
    #     details = validated_data.pop('details')

    #     instance.note = validated_data["note"] if "note" in validated_data else instance.note
    #     if validated_data["status"] == "cancel":
    #         instance.status = "cancel"

    #         for detail in instance.details.all():
    #             WarehouseTransaction.objects.create(
    #                 product=detail.product,
    #                 reference=detail.pk,
    #                 change=+detail.get_quantity_dvtcb(),
    #                 type="order_cancel"
    #             )
    #     instance.save()
    #     return instance

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
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
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
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
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
        obj.order.status = "refund"
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
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = OrderRefund
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
