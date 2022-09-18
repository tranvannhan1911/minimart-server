from rest_framework import serializers

from management.models import InventoryReceivingVoucher, InventoryReceivingVoucherDetail
from management.serializers.product import ProductSerializer, ReadProductSerializer, UnitExchangeSerializer
from management.serializers.supplier import SupplierSerializer


class ResponseInventoryRCDetailSerializer(serializers.ModelSerializer):
    unit_exchange = UnitExchangeSerializer(read_only=True)
    product = ReadProductSerializer(read_only=True)
    class Meta:
        model = InventoryReceivingVoucherDetail
        exclude = ('receiving_voucher', ) 

class ResponseInventoryRCSerializer(serializers.ModelSerializer):
    details = ResponseInventoryRCDetailSerializer(many=True)
    supplier = SupplierSerializer()
    class Meta:
        model = InventoryReceivingVoucher
        fields = '__all__'
        read_only_fiels = ('total', )

class InventoryRCDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryReceivingVoucherDetail
        exclude = ('receiving_voucher', ) 

class InventoryRCSerializer(serializers.ModelSerializer):
    details = InventoryRCDetailSerializer(many=True)
    class Meta:
        model = InventoryReceivingVoucher
        fields = '__all__'
        read_only_fiels = ('total', )

    def create(self, validated_data):
        details = validated_data.pop('details')
        voucher = super().create(validated_data)
        total = 0
        for detail in details:
            detail["receiving_voucher"] = voucher
            total += detail["quantity"]*detail["price"]
            InventoryReceivingVoucherDetail.objects.create(**detail)
        voucher.total = total
        voucher.save()
        return voucher

    def update(self, instance, validated_data):
        details = validated_data.pop('details')
        instance = super().update(instance, validated_data)
        instance.details.all().delete()
        total = 0
        for detail in details:
            detail["receiving_voucher"] = instance
            total += detail["quantity"]*detail["price"]
            InventoryReceivingVoucherDetail.objects.create(**detail)
        instance.total = total
        instance.save()
        return instance