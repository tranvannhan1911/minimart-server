from rest_framework import serializers

from management.models import Supplier
from management.serializers.user import UserSerializer

class SupplierSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }