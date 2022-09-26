from rest_framework import serializers

from management.models import Order, OrderDetail, Promotion, PromotionDetail, PromotionLine

# class PromotionDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PromotionDetail
#         fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        exclude = ('order', )
        read_only_fields = ('total', )
#         read_only_fields = ('date_created', 'user_created', 
#             'date_updated', 'user_updated')


    # def create(self, validated_data):
    #     detail = validated_data.pop('detail')
    #     obj = super().create(validated_data)
    #     detail = PromotionDetail.objects.create(
    #         promotion_line=obj.pk,
    #         **detail)
    #     return obj

    # def update(self, instance, validated_data):
    #     detail = validated_data.pop('detail')
    #     instance = super().update(instance, validated_data)
    #     detail_serializer = PromotionDetailSerializer(instance.detail, data=detail)
    #     detail_serializer.is_valid()
    #     detail_serializer.save()
    #     return instance

class OrderSerializer(serializers.ModelSerializer):
    details = OrderDetailSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')