from rest_framework import serializers

from management.models import Order, OrderDetail, Promotion, PromotionDetail, PromotionLine
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
            detail["order"] = obj
            detail["total"] = detail["quantity"]*detail["price"].price
            detail = OrderDetail.objects.create(**detail)
            total += detail.quantity*detail.price.price
        obj.total = total
        obj.save()
        return obj
        
    def update(self, instance, validated_data):
        details = validated_data.pop('details')
        # instance = super().update(instance, validated_data)
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