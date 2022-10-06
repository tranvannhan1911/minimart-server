

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from management.models import Customer, User, created_updated
from management.serializers.customer import CustomerLoginSerializer
from rest_framework import generics
from management.serializers.user import PhoneSerializer
from management.swagger import SwaggerSchema
from management.utils.apicode import ApiCode
from django.contrib.auth.hashers import (
    make_password,
)
from rest_framework_simplejwt.tokens import RefreshToken
from otp_twilio.models import TwilioSMSDevice

class CustomerLoginView(generics.GenericAPIView):

    # @swagger_auto_schema(
    #     manual_parameters=[SwaggerSchema.token],
    #     request_body=CalculationUnitSerializer,
    #     responses={200: swagger.unit["get"]})
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        print(serializer["phone"])
        if not Customer.objects.filter(phone=serializer.data["phone"]).exists():
            return Response(data = ApiCode.error(message="Số điện thoại không tồn tại"), status = status.HTTP_200_OK)
        
        customer = Customer.objects.get(phone=serializer.data["phone"])
        if customer.is_active == False:
            return Response(data = ApiCode.error(message="Tài khoản đã bị vô hiệu hóa"), status = status.HTTP_200_OK)
        
        if customer.check_password(serializer.data["password"]) == False:
            return Response(data = ApiCode.error(message="Sai mật khẩu"), status = status.HTTP_200_OK)

        refresh = RefreshToken.for_user(customer)

        return Response(data = ApiCode.success(data={
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }), status = status.HTTP_200_OK)


class CustomerForgotPassword(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    # @swagger_auto_schema(responses={200: SwaggerSchema.success()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        number = User.format_phone(serializer.data["phone"])
        phone = User.convert_phone(number)
        print(phone, number)
        if Customer.check_exists(phone) == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer = Customer.objects.get(phone = phone)

        verifier = TwilioSMSDevice()
        verifier.user = User.objects.all().first()
        verifier.generate_challenge()
        # try:
        #     verifier.generate_challenge()
        # except Exception:
        #     return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

# class ForgotPasswordVerify(generics.GenericAPIView):
#     serializer_class = PhoneVerifySerializer

#     @swagger_auto_schema(responses={200: SwaggerSchema.success()})
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid() == False:
#             return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

#         number = User.format_phone(serializer.data["phone"])
#         code = serializer.data["code"]
#         phone = User.convert_phone(number)
#         if (User.check_exists(phone, True) == False or
#             TwilioSMSDevice.objects.filter(number=number, token=code).exists() == False):
#             return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

#         user = User.objects.get(phone = phone)

#         verifier = TwilioSMSDevice.objects.get(number=number, token=code)
#         if verifier.verify_token(code) == False:
#             return Response(data = ApiCode.error(), status = status.HTTP_200_OK)
        
#         new_password = User.random_password()
#         client = MessageClient()
#         client.send_message("Mật khẩu mới của bạn là {0}".format(new_password), number)
#         user.set_password(new_password)
#         user.save()

#         return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
