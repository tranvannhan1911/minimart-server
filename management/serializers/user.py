from rest_framework import serializers
from rest_framework_simplejwt import serializers as serializers_jwt
from management.serializers import ResponeSerializer


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class ResponseTokenSerializer(ResponeSerializer):
    data = TokenSerializer()

class TokenAccessSerializer(serializers.Serializer):
    access = serializers.CharField()

class ResponseTokenAccessSerializer(ResponeSerializer):
    data = TokenAccessSerializer()