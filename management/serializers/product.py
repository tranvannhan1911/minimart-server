from rest_framework import serializers

from management.models import ProductGroup

class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = '__all__'
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }