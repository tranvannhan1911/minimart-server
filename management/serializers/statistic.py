from rest_framework import serializers

from management.models import Order, OrderDetail, OrderRefund, OrderRefundDetail
from management.serializers.product import CategorySerializer, PriceDetailSerializer, ProductGroupSerializer, ReadProductSerializer, UnitExchangeSerializer
from management.serializers.user import CustomerSerializer, ResponseCustomerSerializer, ResponseCustomerWardSerializer, UserSerializer

# class ResponseOrderDetailSerializer(serializers.ModelSerializer):
#     product = ReadProductSerializer(read_only=True)
#     unit_exchange = UnitExchangeSerializer(read_only=True)
#     price = PriceDetailSerializer()
#     class Meta:
#         model = OrderDetail
#         fields = '__all__'

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
    