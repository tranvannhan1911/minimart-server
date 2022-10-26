from pprint import pprint
from rest_framework import serializers
from django.utils import timezone

from management.models import CalculationUnit, HierarchyTree, PriceDetail, PriceList, Product, ProductGroup, UnitExchange
from management.serializers.user import UserSerializer

class ProductGroupSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = ProductGroup
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

class CalculationUnitSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
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
    price = serializers.IntegerField(read_only=True)
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = UnitExchange
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

class UnitExchangeSerializer(serializers.ModelSerializer):
    unit_name = serializers.CharField(source="unit.name", read_only=True)
    unit_code = serializers.CharField(source="unit.code", read_only=True)
    price = serializers.IntegerField(read_only=True)
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = UnitExchange
        exclude = ('product', )
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

####################

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CategoryTreeSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    key = serializers.IntegerField(source="id")
    class Meta:
        model = HierarchyTree
        fields = '__all__'

class CategoryTreeSelectSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)
    value = serializers.IntegerField(source="id")
    label = serializers.CharField(source="name")
    class Meta:
        model = HierarchyTree
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
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

##############################    
class ProductSerializer(serializers.ModelSerializer):
    units = UnitExchangeSerializer(many=True, required=False)
    stock = serializers.IntegerField(read_only=True)
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
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
            # if unit["value"] == 1:
            #     unit["is_base_unit"] = True
            UnitExchange.objects.create(**unit)
        return product

    def update(self, instance, validated_data):
        units = validated_data.pop('units')
        instance = super().update(instance, validated_data)
        # instance.units.clear()
        for unit in instance.units.all():
            try:
                _unit = UnitExchange.objects.get(product=instance.pk, unit=unit.pk, is_active=True)
                _unit.is_active = False
                _unit.save()
            except:
                pass

        for unit in units:
            if not UnitExchange.objects.filter(product=instance.pk, unit=unit["unit"].pk, is_active=True).exists():
                unit["product"] = instance.pk
                unit["unit"] = unit["unit"].pk
                unit = UnitExchangeAllSerializer(data=unit)
                unit.is_valid()
                unit.save()
            else:
                _unit = UnitExchange.objects.get(product=instance.pk, unit=unit["unit"].pk, is_active=True)
                _unit.value = unit["value"]
                _unit.allow_sale = unit["allow_sale"]
                _unit.save()
            
        return instance

####################### 

class SellableSerializer(serializers.Serializer):
    sellable = serializers.BooleanField(required=False)

class PriceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceDetail
        fields = '__all__'
        read_only_fields = ('pricelist', )


# class ProductCalculationUnitSerializer(CalculationUnitSerializer):
#     unit_exchange = serializers.SerializerMethodField()

#     def get_unit_exchange(self, obj):
#         queryset = UnitExchange.objects.filter(product=obj, is_active=True)
#         return UnitExchangeSerializer(queryset, many=True).data    

class ReadProductSerializer(serializers.ModelSerializer):
    product_groups = ProductGroupSerializer(read_only=True, many=True, required=False)
    product_category = CategorySerializer(read_only=True)
    # units = UnitExchangeSerializer(source="unitexchanges", read_only=True, many=True)
    units = serializers.SerializerMethodField()
    stock = serializers.IntegerField(read_only=True)
    base_unit = CalculationUnitSerializer(source="get_base_unit")
    price_detail = PriceDetailSerializer(source="get_price_detail")
    have_price = serializers.BooleanField(source="_have_price")
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = Product
        exclude = ('barcode_image', )
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

    def get_stock(self, obj):
        return obj.stock()

    def get_units(self, obj):
        queryset = UnitExchange.objects.filter(product=obj, is_active=True)
        return UnitExchangeSerializer(queryset, many=True).data

    

        
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
        products = []
        for detail in pricedetails:
            detail["pricelist"] = pricelist
            pricelist_base_unit = detail["product"].get_price_detail()
            detail = PriceDetail.objects.create(**detail)
            products.append(detail.product)

        products = set(products)
        for product in products:
            price_base_unit = product.get_price_detail()
            for unit in product.units.all():
                unit_exchange = product.get_unit_exchange(unit)
                if PriceDetail.objects.filter(
                        unit_exchange=unit_exchange,
                        product=product,
                    ).count() == 0:
                    PriceDetail.objects.create(
                        pricelist=pricelist,
                        unit_exchange=unit_exchange,
                        price=price_base_unit.price*unit_exchange.value,
                        product=product
                    )
                    
        return pricelist

    def update(self, instance, validated_data):
        pricedetails = validated_data.pop('pricedetails')
        instance = super().update(instance, validated_data)
        # instance.pricedetails.all().delete()
        # for detail in pricedetails:
        #     detail["pricelist"] = instance
        #     detail = PriceDetail.objects.create(**detail)
        return instance


class ResponsePriceDetailSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer()
    unit_exchange = UnitExchangeAllSerializer()
    class Meta:
        model = PriceDetail
        fields = '__all__'
        
class ResponsePriceListSerializer(serializers.ModelSerializer):
    pricedetails = ResponsePriceDetailSerializer(many=True)
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = PriceList
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
