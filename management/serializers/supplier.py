from rest_framework import serializers

from management.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }