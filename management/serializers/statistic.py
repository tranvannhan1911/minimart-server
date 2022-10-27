from rest_framework import serializers

from management.models import Order, OrderDetail
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
    