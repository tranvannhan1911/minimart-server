from rest_framework import serializers
from rest_framework_simplejwt import serializers as serializers_jwt
from management.models import User
from management.serializers import ResponeSerializer

class PhoneSerializer(serializers.Serializer):
    so_dien_thoai = serializers.CharField()

class PhoneVerifySerializer(serializers.Serializer):
    so_dien_thoai = serializers.CharField()
    code = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    so_dien_thoai = serializers.CharField()
    mat_khau = serializers.CharField()
    mat_khau_moi = serializers.CharField()

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class ResponseTokenSerializer(ResponeSerializer):
    data = TokenSerializer()

class TokenAccessSerializer(serializers.Serializer):
    access = serializers.CharField()

class ResponseTokenAccessSerializer(ResponeSerializer):
    data = TokenAccessSerializer()