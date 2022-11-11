

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from management.models import Customer, User, OtpCustomer
from management.serializers.customer import CustomerLoginSerializer
from rest_framework import generics
from management.serializers.user import PhoneSerializer, PhoneVerifySerializer, ChangePasswordSerializer
from management.swagger import SwaggerSchema
from management import swagger
from management.utils.apicode import ApiCode
from rest_framework_simplejwt.tokens import RefreshToken
from otp_twilio.models import TwilioSMSDevice
from supermarket.settings import OTP_TWILIO_TOKEN_TEMPLATE
from management.utils.twilio import MessageClient
from drf_yasg.utils import swagger_auto_schema

class CustomerLoginView(generics.GenericAPIView):

    @swagger_auto_schema(
        request_body=CustomerLoginSerializer,
        responses={200: swagger.token})
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        if not Customer.objects.filter(phone=serializer.data["phone"]).exists():
            return Response(data = ApiCode.error(message="Số điện thoại không tồn tại"), status = status.HTTP_200_OK)
        
        customer = Customer.objects.get(phone=serializer.data["phone"])
        if customer.is_active == False:
            return Response(data = ApiCode.error(message="Tài khoản đã bị vô hiệu hóa"), status = status.HTTP_200_OK)
        
        if customer.check_password(serializer.data["password"]) == False:
            return Response(data = ApiCode.error(message="Sai mật khẩu"), status = status.HTTP_200_OK)

        refresh = RefreshToken()
        refresh.payload = {
            "id": customer.id,
            "phone": customer.phone
        }

        return Response(data = ApiCode.success(data={
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }), status = status.HTTP_200_OK)


class CustomerForgotPassword(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    @swagger_auto_schema(
        request_body=PhoneSerializer,
        responses={200: SwaggerSchema.success()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        number = User.format_phone(serializer.data["phone"])
        phone = User.convert_phone(number)
        
        if Customer.check_exists(phone, True) == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer = Customer.objects.get(phone = phone)

        otp = OtpCustomer.generate(customer)
        # try:
        message = OTP_TWILIO_TOKEN_TEMPLATE.format(token=otp)
        number = User.format_phone(customer.phone)
        print(number)
        client = MessageClient()
        client.send_message(message, number)
        # except:
        #     return Response(data = ApiCode.error(message="Có lỗi xảy ra!"), status = status.HTTP_200_OK)
        
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

class CustomerForgotPasswordVerify(generics.GenericAPIView):
    serializer_class = PhoneVerifySerializer

    @swagger_auto_schema(
        request_body=PhoneVerifySerializer,
        responses={200: SwaggerSchema.success()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        phone = serializer.data["phone"]
        code = serializer.data["code"]
        if not Customer.check_exists(phone, True):
            return Response(data = ApiCode.error(message="Số điện thoại không hợp lệ"), status = status.HTTP_200_OK)

        customer = Customer.objects.get(phone = phone)

        if not OtpCustomer.verify(customer, code):
            return Response(data = ApiCode.error(message="OTP không hợp lệ!"), status = status.HTTP_200_OK)

        new_password = customer.random_password()
        try:
            client = MessageClient()
            client.send_message("Mật khẩu mới của bạn là {0}".format(new_password), User.format_phone(phone))
        except Exception as e:
            print("error", e)
            return Response(data = ApiCode.error(message="Có lỗi xảy ra!"), status = status.HTTP_200_OK)

        customer.set_password(new_password)
        customer.save()

        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


class MobileChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer

    @swagger_auto_schema(
        request_body=ChangePasswordSerializer,
        responses={200: SwaggerSchema.success()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        phone = serializer.data["phone"]
        password = serializer.data["password"]
        new_password = serializer.data["new_password"]

        if Customer.check_exists(phone, True) == False:
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer = Customer.objects.get(phone=phone)
        if customer.check_password(password) == False:
            return Response(data = ApiCode.error(message="Sai mật khẩu"), status = status.HTTP_200_OK)
        
        customer.set_password(new_password)
        customer.save()

        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
