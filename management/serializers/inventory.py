from rest_framework import serializers

from management.models import InventoryReceivingVoucher, InventoryReceivingVoucherDetail, InventoryVoucher, InventoryVoucherDetail, OrderDetail, OrderRefund, OrderRefundDetail, Product, WarehouseTransaction
from management.serializers.product import ProductSerializer, ReadProductSerializer, UnitExchangeSerializer
from management.serializers.sell import OrderSerializer, ResponseOrderDetailSerializer, ResponseOrderRefundDetailSerializer, ResponseOrderRefundSerializer, ResponseOrderSerializer
from management.serializers.supplier import SupplierSerializer
from management.serializers.user import UserSerializer


class ResponseInventoryRCDetailSerializer(serializers.ModelSerializer):
    unit_exchange = UnitExchangeSerializer(read_only=True)
    product = ReadProductSerializer(read_only=True)
    class Meta:
        model = InventoryReceivingVoucherDetail
        fields = '__all__'

class ResponseInventoryRCSerializer(serializers.ModelSerializer):
    details = ResponseInventoryRCDetailSerializer(many=True)
    supplier = SupplierSerializer()
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = InventoryReceivingVoucher
        fields = '__all__'
        read_only_fiels = ('total', 'date_created', 'user_created', 
            'date_updated', 'user_updated')

class InventoryRCDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryReceivingVoucherDetail
        exclude = ('receiving_voucher', ) 

class InventoryRCSerializer(serializers.ModelSerializer):
    details = InventoryRCDetailSerializer(many=True)
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = InventoryReceivingVoucher
        fields = '__all__'
        read_only_fiels = ('total', 'date_created', 'user_created', 
            'date_updated', 'user_updated')

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

    def _update_detail(self, instance, validated_data):
        # pending
        details = validated_data.pop('details')
        instance = super().update(instance, validated_data)

        instance.details.all().delete()
        total = 0
        for detail in details:
            detail["receiving_voucher"] = instance
            total += detail["quantity"]*detail["price"]
            irvd = InventoryReceivingVoucherDetail.objects.create(**detail)
            # pending to complete
            if instance.status == "complete":
                print("pending to complete")
                WarehouseTransaction.objects.create(
                    product=detail["product"],
                    reference=irvd.pk,
                    change=detail["quantity"],
                    type="inventory_receiving"
                )
        instance.total = total
        instance.save()
        return instance

    def update(self, instance, validated_data):
        if instance.status == "pending":
            return self._update_detail(instance, validated_data)

        # hủy
        if instance.status == "complete" and validated_data["status"] == "cancel":
            details = validated_data.pop('details')
            instance = super().update(instance, validated_data)
            for detail in instance.details.all():
                WarehouseTransaction.objects.create(
                    product=detail.product,
                    reference=detail.pk,
                    change=-detail.quantity,
                    type="inventory_receiving_cancel"
                )
            return instance
        
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
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = InventoryVoucher
        fields = '__all__'
        read_only_fields = ('date_created', )

# 
class InventoryRecordDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryVoucherDetail
        exclude = ('inventory_voucher', ) 
        read_only_fields = ('quantity_before', )

class InventoryRecordSerializer(serializers.ModelSerializer):
    details = InventoryRecordDetailSerializer(many=True)
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = InventoryVoucher
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

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

    def _update_detail(self, instance, validated_data):
        details = validated_data.pop('details')
        instance = super().update(instance, validated_data)

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

    def update(self, instance, validated_data):
        if instance.status == "pending":
            return self._update_detail(instance, validated_data)

        # hủy
        if instance.status == "complete" and validated_data["status"] == "cancel":
            details = validated_data.pop('details')
            instance = super().update(instance, validated_data)
            for detail in instance.details.all():
                WarehouseTransaction.objects.create(
                    product=detail.product,
                    reference=detail.pk,
                    change=-(detail.quantity_after - detail.quantity_before),
                    type="inventory_cancel"
                )
            return instance
        
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
            print(obj.reference)
            _obj = OrderDetail.objects.get(pk = obj.reference)
            _obj = ResponseOrderDetailSerializer(_obj).data
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
            _obj = InventoryReceivingVoucherDetail.objects.get(pk = obj.reference)
            _obj = ResponseInventoryRCDetailSerializer(_obj).data
        elif obj.type == "refund":
            _obj = OrderRefundDetail.objects.get(pk = obj.reference)
            _obj = ResponseOrderRefundDetailSerializer(_obj).data
        return _obj

    def get_type(self, obj):
        return {
            "type": obj.type,
            "type_name": obj.get_type_display()
        }