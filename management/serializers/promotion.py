from rest_framework import serializers

from management.models import Promotion

class PromitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'