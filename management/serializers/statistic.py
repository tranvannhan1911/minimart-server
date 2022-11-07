from dataclasses import field
from rest_framework import serializers

from management.models import (
    Customer, InventoryReceivingVoucherDetail, Order, 
    OrderDetail, OrderRefund, OrderRefundDetail, 
    Promotion, PromotionHistory, PromotionLine, 
    WarehouseTransaction, PromotionDetail
)
from management.serializers.product import (
    CategorySerializer, PriceDetailSerializer, 
    ProductGroupSerializer, ReadProductSerializer, 
    UnitExchangeSerializer, ShortResponseProductSerializer
)
from management.serializers.promotion import PromotionDetailSerializer
from management.serializers.sell import ResponseOrderSerializer
from management.serializers.user import CustomerSerializer, ResponseCustomerSerializer, ResponseCustomerWardSerializer, UserSerializer
from django.db.models import Sum

class ResponseShortCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('password', 'customer_group', 'user_created',
            'user_updated')



class ShortResponseOrderDetailSerializer(serializers.ModelSerializer):
    product = ShortResponseProductSerializer(read_only=True)
    unit_exchange = UnitExchangeSerializer(read_only=True)
    price = PriceDetailSerializer()
    class Meta:
        model = OrderDetail
        fields = '__all__'

class ShortResponseOrderSerializer(serializers.ModelSerializer):
    details = ShortResponseOrderDetailSerializer(many=True)
    customer = serializers.CharField(source="customer.fullname")
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"

class StatisticTop5CustomerSerializer(serializers.Serializer):
    total = serializers.FloatField()
    final_total = serializers.FloatField()
    count = serializers.IntegerField()
    customer = ResponseShortCustomerSerializer()

class StatisticOrder7DaysSerializer(serializers.Serializer):
    date = serializers.CharField()
    total = serializers.FloatField()
    final_total = serializers.FloatField()
    count = serializers.IntegerField()

class StatisticDashboardSerializer(serializers.Serializer):
    top_5_order = ShortResponseOrderSerializer(many=True)
    top_5_customer = StatisticTop5CustomerSerializer(many=True)
    order_7_days = StatisticOrder7DaysSerializer(many=True)
    
    count_order_7_days = serializers.IntegerField()
    count_order_refund_7_days = serializers.IntegerField()
    total_money_7_days = serializers.IntegerField()
    count_customer_7_days = serializers.IntegerField()

################################
class StatisticSellSerializer(serializers.Serializer):
    user_created = UserSerializer(read_only=True)
    date_created = serializers.DateTimeField()
    discount = serializers.FloatField()
    total = serializers.FloatField()
    final_total = serializers.FloatField()

class StatisticSalesCustomerSerializer(serializers.Serializer):
    customer = ResponseCustomerWardSerializer(read_only=True)
    product_groups = ProductGroupSerializer()
    product_category = CategorySerializer()
    discount = serializers.FloatField()
    total = serializers.FloatField()
    final_total = serializers.FloatField()

#########################

class ResponseOrderNotDetailsSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

class ResponseOrderRefundNotDetailsSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = OrderRefund
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

class StatisticRefundSerializer(serializers.ModelSerializer):
    order_refund = ResponseOrderRefundNotDetailsSerializer()
    order = ResponseOrderNotDetailsSerializer(source="order_refund.order")
    customer = CustomerSerializer(source="order_refund.order.customer")
    product = ReadProductSerializer(read_only=True)
    unit_exchange = UnitExchangeSerializer(read_only=True)
    class Meta:
        model = OrderRefundDetail
        fields = '__all__'

##################

class StatisticPromitionSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = Promotion
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

class StatisticPromotionDetailSerializer(serializers.ModelSerializer):
    product_received = ShortResponseProductSerializer()
    class Meta:
        model = PromotionDetail
        fields = '__all__'

class StatisticPromotionLineSerializer(serializers.ModelSerializer):
    detail = StatisticPromotionDetailSerializer()
    remain = serializers.IntegerField(source="get_remain", read_only=True)
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    promotion = StatisticPromitionSerializer()
    total_discounted = serializers.SerializerMethodField()
    count_product_received = serializers.SerializerMethodField()
    class Meta:
        model = PromotionLine
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

    def get_total_discounted(self, obj):
        total = PromotionHistory.objects.filter(
                promotion_line = obj
            ).aggregate(Sum("amount"))["amount__sum"]
        return total
    
    def get_count_product_received(self, obj):
        # count = PromotionHistory.objects.filter(
        #         promotion_line = obj
        #     ).aggregate(Sum("amount"))["amount__sum"]
        return 0

    
class StatisticPromotionHistorySerializer(serializers.ModelSerializer):
    promotion_line = StatisticPromotionLineSerializer()
    quantity_used = serializers.IntegerField(read_only=True)
    quantity_product_received = serializers.IntegerField(read_only=True)
    class Meta:
        model = PromotionHistory
        exclude = ('note', 'order', 'buy_order_detail', 'received_order_detail')
            
################################
class StatisticInventoryReceivingSerializer(serializers.ModelSerializer):
    # promotion_line = StatisticPromotionLineSerializer()
    total = serializers.FloatField()
    product = ReadProductSerializer()
    class Meta:
        model = InventoryReceivingVoucherDetail
        exclude = ('quantity', 'price', 'receiving_voucher', 'unit_exchange')


################################
class StatisticStockSerializer(serializers.ModelSerializer):
    # promotion_line = StatisticPromotionLineSerializer()
    stock_base_unit = serializers.IntegerField()
    product = ReadProductSerializer()
    class Meta:
        model = WarehouseTransaction
        exclude = ('reference', 'change', 'type', 'date_created', 'note')