from pprint import pprint
from rest_framework import serializers

from management.models import CalculationUnit, HierarchyTree, PriceDetail, PriceList, Product, ProductGroup, UnitExchange

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

class CalculationUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationUnit
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }
###############################
class UnitExchangeAllSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    class Meta:
        model = UnitExchange
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

class UnitExchangeSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    class Meta:
        model = UnitExchange
        exclude = ('product', )
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

##############################    
class ProductSerializer(serializers.ModelSerializer):
    units = UnitExchangeSerializer(many=True, required=False)
    stock = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        exclude = ('barcode_image', )
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

    def get_stock(self, obj):
        return obj.stock()

    def create(self, validated_data):
        units = validated_data.pop('units')
        product = super().create(validated_data)
        for unit in units:
            unit["product"] = product
            UnitExchange.objects.create(**unit)
        return product

    def update(self, instance, validated_data):
        units = validated_data.pop('units')
        instance = super().update(instance, validated_data)
        # instance.units.clear()
        for unit in instance.units.all():
            _unit = UnitExchange.objects.get(product=instance.pk, unit=unit.pk)
            try:
                _unit.delete()
            except:
                pass

        for unit in units:
            if not UnitExchange.objects.filter(product=instance.pk, unit=unit["unit"].pk).exists():
                unit["product"] = instance.pk
                unit["unit"] = unit["unit"].pk
                unit = UnitExchangeAllSerializer(data=unit)
                unit.is_valid()
                unit.save()
            else:
                _unit = UnitExchange.objects.get(product=instance.pk, unit=unit["unit"].pk)
                _unit.value = unit["value"]
                _unit.allow_sale = unit["allow_sale"]
                _unit.save()
            
        return instance

####################### 
class PriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceDetail
        fields = '__all__'
        read_only_fields = ('pricelist', )
        
class ReadProductSerializer(serializers.ModelSerializer):
    product_groups = ProductGroupSerializer(read_only=True, many=True, required=False)
    units = UnitExchangeSerializer(source="unitexchanges", read_only=True, many=True)
    stock = serializers.IntegerField(read_only=True)
    base_unit = CalculationUnitSerializer(source="get_base_unit")
    price_detail = PriceDetailSerializer(source="get_price_detail")
    class Meta:
        model = Product
        exclude = ('barcode_image', )
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

    def get_stock(self, obj):
        return obj.stock()

        
class PriceListSerializer(serializers.ModelSerializer):
    pricedetails = PriceDetailSerializer(many=True)
    class Meta:
        model = PriceList
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

    def create(self, validated_data):
        pricedetails = validated_data.pop('pricedetails')
        pricelist = super().create(validated_data)
        for detail in pricedetails:
            detail["pricelist"] = pricelist
            PriceDetail.objects.create(**detail)
        return pricelist

    def update(self, instance, validated_data):
        pricedetails = validated_data.pop('pricedetails')
        instance = super().update(instance, validated_data)
        instance.pricedetails.all().delete()
        for detail in pricedetails:
            detail["pricelist"] = instance
            detail = PriceDetail.objects.create(**detail)
        return instance


class ResponsePriceDetailSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer()
    unit_exchange = UnitExchangeAllSerializer()
    class Meta:
        model = PriceDetail
        fields = '__all__'
        
class ResponsePriceListSerializer(serializers.ModelSerializer):
    pricedetails = ResponsePriceDetailSerializer(many=True)
    class Meta:
        model = PriceList
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
####################

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CategoryTreeSerializer(serializers.ModelSerializer):
    childs = RecursiveField(many=True)
    class Meta:
        model = HierarchyTree
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HierarchyTree
        fields = '__all__'
        read_only_fields = ('type', 'level', 'date_created', 'user_created', 
            'date_updated', 'user_updated')

    def create(self, validated_data):
        category = super().create(validated_data)
        level = 0
        if category.parent != None:
            level = category.parent.level + 1
        category.level = level
        category.type = "product"
        category.save()
        return category


    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        level = 0
        if instance.parent != None:
            level = instance.parent.level + 1
        instance.level = level
        instance.type = "product"
        instance.save()
        return instance

    