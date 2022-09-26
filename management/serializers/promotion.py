from rest_framework import serializers

from management.models import Promotion, PromotionDetail, PromotionLine

class PromotionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionDetail
        fields = '__all__'


class PromotionLineSerializer(serializers.ModelSerializer):
    detail = PromotionDetailSerializer()
    class Meta:
        model = PromotionLine
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')


    def create(self, validated_data):
        detail = validated_data.pop('detail')
        obj = super().create(validated_data)

        applicable_product_groups = detail.pop("applicable_product_groups")
        applicable_products = detail.pop("applicable_products")
        detail = PromotionDetail.objects.create(
            promotion_line=obj,
            **detail)
        for product_group in applicable_product_groups:
            detail.applicable_product_groups.add(product_group)
        for product in applicable_products:
            detail.applicable_products.add(product)
        return obj

    def update(self, instance, validated_data):
        detail = validated_data.pop('detail')
        instance = super().update(instance, validated_data)
        detail_serializer = PromotionDetailSerializer(instance.detail, data=detail)
        detail_serializer.is_valid()
        detail_serializer.save()
        return instance

class PromitionSerializer(serializers.ModelSerializer):
    lines = PromotionLineSerializer(many=True, read_only=True)
    class Meta:
        model = Promotion
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')