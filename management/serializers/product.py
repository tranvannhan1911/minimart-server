from pprint import pprint
from rest_framework import serializers

from management.models import CalculationUnit, PriceDetail, PriceList, Product, ProductGroup, UnitExchange

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

class CalculationUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationUnit
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

class UnitExchangeAllSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    class Meta:
        model = UnitExchange
        fields = '__all__'

class UnitExchangeSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    class Meta:
        model = UnitExchange
        exclude = ('product', )
        
class ProductSerializer(serializers.ModelSerializer):
    units = UnitExchangeSerializer(many=True, required=False)
    class Meta:
        model = Product
        exclude = ('barcode_image', )

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

class ReadProductSerializer(serializers.ModelSerializer):
    product_groups = ProductGroupSerializer(read_only=True, many=True, required=False)
    units = UnitExchangeSerializer(source="unitexchanges", read_only=True, many=True)
    class Meta:
        model = Product
        exclude = ('barcode_image', )

class ReadProductSerializer(serializers.ModelSerializer):
    product_groups = ProductGroupSerializer(read_only=True, many=True, required=False)
    units = UnitExchangeSerializer(source="unitexchanges", read_only=True, many=True)
    class Meta:
        model = Product
        exclude = ('barcode_image', )

class PriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceDetail
        exclude = ('pricelist', ) 
        
class PriceListSerializer(serializers.ModelSerializer):
    pricedetails = PriceDetailSerializer(many=True)
    class Meta:
        model = PriceList
        fields = '__all__'

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