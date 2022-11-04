
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from management.models import Customer, User, created_updated
from management.serializers.user import ResponseCustomerSerializer
from rest_framework import generics
from management.serializers.user import PhoneSerializer
from management.swagger import SwaggerSchema
from management import swagger
from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import (
    make_password,
)
from rest_framework_simplejwt.tokens import RefreshToken
from otp_twilio.models import TwilioSMSDevice
from management.utils.token_decorator import token_required

class MobileCustomerView(generics.GenericAPIView):

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.customer["get"]})
    @token_required
    def get(self, request):
        response = ResponseCustomerSerializer(request.customer)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)
