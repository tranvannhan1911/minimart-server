from rest_framework import serializers

from management.models import InventoryReceivingVoucher, InventoryReceivingVoucherDetail, InventoryVoucher, InventoryVoucherDetail, Product, WarehouseTransaction
from management.serializers.product import ProductSerializer, ReadProductSerializer, UnitExchangeSerializer
from management.serializers.supplier import SupplierSerializer


class ResponseInventoryRCDetailSerializer(serializers.ModelSerializer):
    unit_exchange = UnitExchangeSerializer(read_only=True)
    product = ReadProductSerializer(read_only=True)
    class Meta:
        model = InventoryReceivingVoucherDetail
        fields = '__all__'

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
            irvd = InventoryReceivingVoucherDetail.objects.create(**detail)
            if voucher.status == "complete":
                WarehouseTransaction.objects.create(
                    product=detail["product"],
                    reference=irvd.pk,
                    change=detail["quantity"],
                    type="inventory_receiving"
                )
        voucher.total = total
        voucher.save()
        return voucher

    def update(self, instance, validated_data):
        if instance.status == "complete":
            already_complete = True

        details = validated_data.pop('details')
        instance = super().update(instance, validated_data)
        if validated_data["status"] == "cancel":
            for detail in instance.details.all():
                WarehouseTransaction.objects.create(
                    product=detail.product,
                    reference=detail.pk,
                    change=-detail.quantity,
                    type="inventory_receiving_cancel"
                )
            return instance
        
        if already_complete:
            return instance

        instance.details.all().delete()
        total = 0
        for detail in details:
            detail["receiving_voucher"] = instance
            total += detail["quantity"]*detail["price"]
            irvd = InventoryReceivingVoucherDetail.objects.create(**detail)
            if instance.status == "complete":
                WarehouseTransaction.objects.create(
                    product=detail["product"],
                    reference=irvd.pk,
                    change=detail["quantity"],
                    type="inventory_receiving"
                )
        instance.total = total
        instance.save()
        return instance

##############################################

# response
class ResponseInventoryRecordDetailSerializer(serializers.ModelSerializer):
    unit_exchange = UnitExchangeSerializer(read_only=True)
    product = ReadProductSerializer(read_only=True)
    class Meta:
        model = InventoryVoucherDetail
        fields = '__all__'

class ResponseInventoryRecordSerializer(serializers.ModelSerializer):
    details = ResponseInventoryRecordDetailSerializer(many=True)
    class Meta:
        model = InventoryVoucher
        fields = '__all__'

# 
class InventoryRecordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryVoucherDetail
        exclude = ('inventory_voucher', ) 
        read_only_fields = ('quantity_before', )

class InventoryRecordSerializer(serializers.ModelSerializer):
    details = InventoryRecordDetailSerializer(many=True)
    class Meta:
        model = InventoryVoucher
        fields = '__all__'

    def create(self, validated_data):
        details = validated_data.pop('details')
        voucher = super().create(validated_data)
        for detail in details:
            detail["inventory_voucher"] = voucher
            
            detail["quantity_before"] = detail["product"].stock()
            _detail = InventoryVoucherDetail.objects.create(**detail)
            if voucher.status == "complete":
                WarehouseTransaction.objects.create(
                    product=detail["product"],
                    reference=_detail.pk,
                    change=detail["quantity_after"]-detail["quantity_before"],
                    type="inventory"
                )
        return voucher

    def update(self, instance, validated_data):
        if instance.status == "complete":
            already_complete = True

        details = validated_data.pop('details')
        instance = super().update(instance, validated_data)
        if validated_data["status"] == "cancel":
            for detail in instance.details.all():
                WarehouseTransaction.objects.create(
                    product=detail.product,
                    reference=detail.pk,
                    change=-(detail.quantity_after - detail.quantity_before),
                    type="inventory_cancel"
                )
            return instance
        
        if already_complete:
            return instance

        instance.details.all().delete()
        for detail in details:
            detail["inventory_voucher"] = instance
            
            detail["quantity_before"] = detail["product"].stock()
            _detail = InventoryVoucherDetail.objects.create(**detail)
            if instance.status == "complete":
                WarehouseTransaction.objects.create(
                    product=detail["product"],
                    reference=_detail.pk,
                    change=detail["quantity_after"]-detail["quantity_before"],
                    type="inventory"
                )
        return instance

####################################
class ResponseWarehouseTransactionSerializer(serializers.ModelSerializer):
    product = ReadProductSerializer(read_only=True)
    reference = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WarehouseTransaction
        fields = '__all__'

    def get_reference(self, obj):
        _obj = None
        if obj.type == "order":
            _obj = None
        elif obj.type == "inventory":
            _obj = InventoryVoucherDetail.objects.get(pk = obj.reference)
            _obj = ResponseInventoryRecordDetailSerializer(_obj).data
        elif obj.type == "inventory_cancel":
            _obj = InventoryVoucherDetail.objects.get(pk = obj.reference)
            _obj = ResponseInventoryRecordDetailSerializer(_obj).data
        elif obj.type == "inventory_receiving":
            _obj = InventoryReceivingVoucherDetail.objects.get(pk = obj.reference)
            _obj = ResponseInventoryRCDetailSerializer(_obj).data
        elif obj.type == "inventory_receiving_cancel":
            _obj = None
        elif obj.type == "refund":
            _obj = None
        return _obj

    def get_type(self, obj):
        return {
            "type": obj.type,
            "type_name": obj.get_type_display()
        }