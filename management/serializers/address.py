from rest_framework import serializers
from rest_framework_simplejwt import serializers as serializers_jwt
from management.models import Customer, CustomerGroup, User
from management.serializers import ResponeSerializer
from vi_address.models import City, District, Ward

class WardAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = '__all__'

class WardSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(source="id")
    label = serializers.CharField(source="name")
    class Meta:
        model = Ward
        fields = ('value', 'label')

class DistrictSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    value = serializers.IntegerField(source="id")
    label = serializers.CharField(source="name")
    class Meta:
        model = District
        fields = ('value', 'label', 'children')

    def get_children(self, obj):
        query = Ward.objects.filter(parent_code=obj.id)
        serializer = WardSerializer(query, many=True)
        return serializer.data

class AddressSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    value = serializers.IntegerField(source="id")
    label = serializers.CharField(source="name")
    class Meta:
        model = City
        fields = ('value', 'label', 'children')

    def get_children(self, obj):
        query = District.objects.filter(parent_code=obj.id)
        serializer = DistrictSerializer(query, many=True)
        return serializer.data