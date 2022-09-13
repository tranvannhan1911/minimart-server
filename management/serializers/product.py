from rest_framework import serializers

from management.models import CalculationUnit, Product, ProductGroup, UnitExchange

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
    class Meta:
        model = UnitExchange
        fields = '__all__'

class UnitExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitExchange
        fields = ('unit', 'value', 'allow_sale')
        
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
        instance.units.clear()
        for unit in units:
            unit["product"] = instance.pk
            unit["unit"] = unit["unit"].pk
            unit = UnitExchangeAllSerializer(data=unit)
            unit.is_valid()
            unit.save()
        return instance

class ReadProductSerializer(serializers.ModelSerializer):
    product_groups = ProductGroupSerializer(read_only=True, many=True, required=False)
    units = UnitExchangeSerializer(source="unitexchanges", read_only=True, many=True)
    class Meta:
        model = Product
        exclude = ('barcode_image', )