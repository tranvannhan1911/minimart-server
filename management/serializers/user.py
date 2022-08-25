from rest_framework import serializers
from rest_framework_simplejwt import serializers as serializers_jwt
from management.models import User
from management.serializers import ResponeSerializer

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()

class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    new_password = serializers.CharField()

############# response ################
class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class ResponseTokenSerializer(ResponeSerializer):
    data = TokenSerializer()

class TokenAccessSerializer(serializers.Serializer):
    access = serializers.CharField()

class ResponseTokenAccessSerializer(ResponeSerializer):
    data = TokenAccessSerializer()