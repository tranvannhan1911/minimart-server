import json
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from rest_framework import permissions
from management import serializers

from management.models import Customer, User

from management.serializers.user import (
    CustomerSerializer, ReadCustomerSerializer, 
    ResponseCustomerSerializer, UpdateCustomerSerializer
)
from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.user import  SwaggerUserSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

class AddCustomerView(generics.GenericAPIView):
    serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_info()})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        if User.objects.filter(phone=serializer.validated_data["account"]["phone"]).exists():
            return Response(data = ApiCode.error(message="Số điện thoại bị trùng"), status = status.HTTP_200_OK)
        # try:
        serializer.save()
        # except Exception:
        #     return Response(data = ApiCode.error(message={"phone": ["duplicated"]}), status = status.HTTP_200_OK)

        customer = Customer.objects.get(account__phone=serializer.data["phone"])
        response = ReadCustomerSerializer(customer)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

class UpdateCustomerView(generics.GenericAPIView):
    serializer_class = UpdateCustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_info()})
        
    def put(self, request, customer_id):
        customer = get_object_or_404(Customer, customer_id=customer_id)
        serializer = self.get_serializer(customer, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        customer = serializer.save()
        customer = Customer.objects.get(customer_id=customer.customer_id)

        response = ReadCustomerSerializer(customer)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

class GetCustomerView(generics.RetrieveAPIView):
    # serializer_class = CustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_info()})
        
    def get(self, request, customer_id):
        if not Customer.objects.filter(customer_id=customer_id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer = Customer.objects.get(customer_id=customer_id)
        response = ReadCustomerSerializer(customer)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)
 
class DeleteCustomerView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})

    def delete(self, request, customer_id):
        if not Customer.objects.filter(customer_id=customer_id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer = Customer.objects.get(customer_id=customer_id)
        account = User.objects.get(customer=customer)
        try:
            account.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa khách hàng này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


class ListCustomerView(generics.GenericAPIView):
    serializer_class = ReadCustomerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Customer.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_list})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = self.get_serializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)
