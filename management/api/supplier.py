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

from management.models import Supplier, User
from management.serializers.supplier import SupplierSerializer
from management.utils import perms

from management.serializers.user import (
    AddUserSerializer, UpdateUserSerializer, UserSerializer, 
    # ResponseCustomerSerializer, UpdateCustomerSerializer
)
from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.user import  SwaggerUserSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

from management.utils.perms import method_permission_classes
from rest_framework import exceptions

class SupplierView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=SupplierSerializer,
        responses={200: SwaggerUserSchema.supplier_get})
    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        supplier = serializer.save()
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return Supplier.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.supplier_list})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = SupplierSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class SupplierIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=SupplierSerializer,
        responses={200: SwaggerUserSchema.supplier_get})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not Supplier.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Nhà cung cấp không tồn tại"), status = status.HTTP_200_OK)

        supplier = Supplier.objects.get(pk = id)
        serializer = SupplierSerializer(supplier, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        supplier = serializer.save()

        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.supplier_get})
    @method_permission_classes((perms.IsOwnUserOrAdmin, ))
    def get(self, request, id):
        if not Supplier.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Nhà cung cấp không tồn tại"), status = status.HTTP_200_OK)

        supplier = Supplier.objects.get(pk = id)
        serializer = SupplierSerializer(supplier)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not Supplier.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Nhà cung cấp không tồn tại"), status = status.HTTP_200_OK)

        supplier = Supplier.objects.get(pk = id)

        try:
            supplier.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa nhà cung cấp này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
