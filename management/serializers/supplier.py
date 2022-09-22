from rest_framework import serializers

from management.models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('date_created', )
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }