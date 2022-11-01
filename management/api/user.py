import json
from pprint import pprint
from django.shortcuts import get_object_or_404
from django.urls import resolve
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from rest_framework import permissions
from management import serializers
from management import swagger

from management.models import Customer, User, created_updated
from management.utils import perms

from management.serializers.user import (
    AddUserSerializer, CustomerSerializer, ResponseCustomerSerializer, UpdateUserSerializer, UserSerializer, 
    # ResponseCustomerSerializer, UpdateCustomerSerializer
)
from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.user import  SwaggerUserSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

from management.utils.perms import method_permission_classes
from rest_framework import exceptions
from supermarket.settings import MESSAGE_PASSWORD_TWILIO_TEMPLATE
from management.utils.twilio import MessageClient

class StaffView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=AddUserSerializer,
        responses={200: SwaggerUserSchema.customer_info()})
    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        if User.objects.filter(phone=serializer.validated_data["phone"]).exists():
            return Response(data = ApiCode.error(message="Số điện thoại bị trùng"), status = status.HTTP_200_OK)

        user = serializer.save()
        user.is_staff = True

        raw_password = User.random_password()
        user.set_password(raw_password)
        user.save()
        created_updated(user, request)

        response = UserSerializer(user)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return User.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_list})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        response = UserSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class StaffIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=UpdateUserSerializer,
        responses={200: SwaggerUserSchema.customer_info()})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):

        user = get_object_or_404(User, id=id)
        serializer = UpdateUserSerializer(user, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        user = serializer.save()
        created_updated(user, request)

        response = UserSerializer(user)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_info()})
    @method_permission_classes((perms.IsOwnUserOrAdmin, ))
    def get(self, request, id):
        if not User.objects.filter(id=id).exists():
            return Response(data = ApiCode.error(message="Không tồn tại người dùng này"), status = status.HTTP_200_OK)

        customer = User.objects.get(id=id)
        response = UserSerializer(customer)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not User.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        user = User.objects.get(pk=id)
        try:
            user.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa người dùng này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @method_permission_classes((perms.IsOwnUserOrAdmin, ))
    def get(self, request, id):
        if not User.objects.filter(id=id).exists():
            return Response(data = ApiCode.error(message="Không tồn tại người dùng này"), status = status.HTTP_200_OK)

        user = User.objects.get(id=id)
        raw_password = User.random_password()
        user.set_password(raw_password)
        user.save()

        try:
            message = MESSAGE_PASSWORD_TWILIO_TEMPLATE.format(password=raw_password)
            number = User.format_phone(user.phone)
            client = MessageClient()
            client.send_message(message, number)
        except:
            pass

        response = UserSerializer(user)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)


#########################################

class CustomerView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=CustomerSerializer,
        responses={200: swagger.customer["get"]})
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        if Customer.objects.filter(phone=serializer.validated_data["phone"]).exists():
            return Response(data = ApiCode.error(message="Số điện thoại bị trùng"), status = status.HTTP_200_OK)

        customer = serializer.save()
        raw_password = customer.set_password()
        customer.save()

        message = MESSAGE_PASSWORD_TWILIO_TEMPLATE.format(password=raw_password)
        number = User.format_phone(customer.phone)
        client = MessageClient()
        client.send_message(message, number)

        created_updated(customer, request)

        response = ResponseCustomerSerializer(customer)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return Customer.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.customer["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        response = ResponseCustomerSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class CustomerIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=CustomerSerializer,
        responses={200: swagger.customer["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not Customer.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(message="Khách hàng không tồn tại"), status = status.HTTP_200_OK)

        user = Customer.objects.get(id=id)
        serializer = CustomerSerializer(user, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        user = serializer.save()
        created_updated(user, request)

        response = ResponseCustomerSerializer(user)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.customer["get"]})
    @method_permission_classes((perms.IsOwnUserOrAdmin, ))
    def get(self, request, id):
        if not Customer.objects.filter(id=id).exists():
            return Response(data = ApiCode.error(message="Khách hàng không tồn tại"), status = status.HTTP_200_OK)

        customer = Customer.objects.get(id=id)
        response = ResponseCustomerSerializer(customer)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not Customer.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(message="Khách hàng không tồn tại"), status = status.HTTP_200_OK)

        user = Customer.objects.get(pk=id)
        try:
            user.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa khách hàng này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
