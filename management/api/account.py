from management import serializers
from management.models import User
from management.serializers.user import ChangePasswordSerializer, PhoneSerializer, PhoneVerifySerializer, ResponseTokenAccessSerializer, ResponseTokenSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from otp_twilio.models import TwilioSMSDevice

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings
from drf_yasg.utils import swagger_auto_schema

from management.utils.apicode import ApiCode
from management.utils.swagger import SwaggerSchema
from management.utils.twilio import MessageClient

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

    @swagger_auto_schema(responses={200: ResponseTokenSerializer})
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
        return ApiCode.success(data=data)

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer
    
    @swagger_auto_schema(responses={200: ResponseTokenAccessSerializer})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class ForgotPassword(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    @swagger_auto_schema(responses={200: SwaggerSchema.success()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        number = User.format_phone(serializer.data["so_dien_thoai"])
        so_dien_thoai = User.convert_phone(number)
        if User.check_exists(so_dien_thoai, True) == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        user = User.objects.get(so_dien_thoai = so_dien_thoai)

        verifier = TwilioSMSDevice()
        verifier.number = number
        verifier.user = user
        try:
            verifier.generate_challenge()
        except:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

class ForgotPasswordVerify(generics.GenericAPIView):
    serializer_class = PhoneVerifySerializer

    @swagger_auto_schema(responses={200: SwaggerSchema.success()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        number = User.format_phone(serializer.data["so_dien_thoai"])
        code = serializer.data["code"]
        so_dien_thoai = User.convert_phone(number)
        if (User.check_exists(so_dien_thoai, True) == False or
            TwilioSMSDevice.objects.filter(number=number, token=code).exists() == False):
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        user = User.objects.get(so_dien_thoai = so_dien_thoai)

        verifier = TwilioSMSDevice.objects.get(number=number, token=code)
        if verifier.verify_token(code) == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)
        
        new_password = User.random_password()
        client = MessageClient()
        client.send_message("Mật khẩu mới của bạn là {0}".format(new_password), number)
        user.set_password(new_password)
        user.save()

        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(responses={200: SwaggerSchema.success()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        so_dien_thoai = serializer.data["so_dien_thoai"]
        mat_khau = serializer.data["mat_khau"]
        mat_khau_moi = serializer.data["mat_khau_moi"]

        if User.check_exists(so_dien_thoai, True) == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        user = User.objects.get(so_dien_thoai=so_dien_thoai)
        if user.check_password(mat_khau) == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)
        
        user.set_password(mat_khau_moi)
        user.save()

        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)