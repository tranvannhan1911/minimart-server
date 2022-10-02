from rest_framework import serializers

from management.models import Promotion, PromotionDetail, PromotionLine

class PromotionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionDetail
        fields = '__all__'

    # def update(self, instance, validated_data):
        
    #     instance = super().update(instance, validated_data)
    #     # instance
    #     return instance


class PromotionLineSerializer(serializers.ModelSerializer):
    detail = PromotionDetailSerializer()
    remain = serializers.IntegerField(source="get_remain", read_only=True)
    remain_today = serializers.IntegerField(read_only=True)
    remain_customer = serializers.IntegerField(read_only=True)
    class Meta:
        model = PromotionLine
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')


    def create(self, validated_data):
        detail = validated_data.pop('detail')
        obj = super().create(validated_data)

        applicable_product_groups = []
        applicable_products = []
        if "applicable_product_groups" in detail.keys():
            applicable_product_groups = detail.pop("applicable_product_groups")

        if "applicable_products" in detail.keys():
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
        
        applicable_product_groups = []
        _applicable_product_groups = []
        applicable_products = []
        _applicable_products = []
        product_received = None
        if "applicable_product_groups" in detail.keys():
            applicable_product_groups = detail.pop("applicable_product_groups")
            for x in applicable_product_groups:
                _applicable_product_groups.append(x.pk)

        if "applicable_products" in detail.keys():
            applicable_products = detail.pop("applicable_products")
            for x in applicable_products:
                _applicable_products.append(x.pk)

        if "product_received" in detail.keys():
            product_received = detail.pop("product_received")

        detail_serializer = PromotionDetailSerializer(instance.detail, data=detail)
        detail_serializer.is_valid()
        detail = detail_serializer.save()
        detail.applicable_product_groups.set(_applicable_product_groups)
        detail.applicable_products.set(_applicable_products)
        detail.product_received = product_received
        detail.save()
        return instance

# class PromotionLineBenefitSerializer(PromotionLineSerializer):
#     benefit = serializers.IntegerField(source="")

class PromitionSerializer(serializers.ModelSerializer):
    lines = PromotionLineSerializer(many=True, read_only=True)
    class Meta:
        model = Promotion
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
            
class PromitionByProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    
class PromitionByOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    customer_id = serializers.IntegerField()