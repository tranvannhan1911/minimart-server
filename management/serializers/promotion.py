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


    def create(self, validated_data):
        detail = validated_data.pop('detail')
        object = super().create(validated_data)
        detail = PromotionDetail.objects.create(
            promotion_line=object,
            **detail)
        return object

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