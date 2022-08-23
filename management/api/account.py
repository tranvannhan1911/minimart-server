from management.serializers.user import ResponseTokenAccessSerializer, ResponseTokenSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from drf_yasg.utils import swagger_auto_schema

from management.utils.apicode import ApiCode

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return ApiCode.success(data={
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })


class TokenLoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    @swagger_auto_schema(responses={201: ResponseTokenSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        return ApiCode.success(data=data["access"])

class MyTokenRefreshView(TokenRefreshView):
    # _serializer_class = MyTokenRefreshSerializer
    
    @swagger_auto_schema(responses={201: ResponseTokenAccessSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)