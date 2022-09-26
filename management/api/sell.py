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

from management.models import CalculationUnit, HierarchyTree, Order, PriceList, Product, ProductGroup, Promotion, PromotionLine, Supplier, User, created_updated
from management.serializers.product import CalculationUnitSerializer, CategorySerializer, CategoryTreeSerializer, PriceListSerializer, ProductGroupSerializer, ProductSerializer, ReadProductSerializer
from management.serializers.promotion import PromitionSerializer, PromotionLineSerializer
from management.serializers.sell import OrderSerializer, ResponseOrderSerializer
from management.utils import perms
from management.serializers.user import (
    AddUserSerializer, UpdateUserSerializer, UserSerializer, 
    # ResponseCustomerSerializer, UpdateCustomerSerializer
)
from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

from management.utils.perms import method_permission_classes
from rest_framework import exceptions

class OrderView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=OrderSerializer,
        responses={200: swagger.order["get"]})
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        obj = serializer.save()
        created_updated(obj, request)
        response = ResponseOrderSerializer(obj)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return Order.objects.filter()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.order["get"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = ResponseOrderSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class OrderIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=PromitionSerializer,
        responses={200: swagger.order["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not Order.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Đơn hàng không tồn tại"), status = status.HTTP_200_OK)

        obj = Order.objects.get(pk = id)
        serializer = OrderSerializer(obj, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        obj = serializer.save()
        created_updated(obj, request)
        response = ResponseOrderSerializer(obj)

        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.order["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not Order.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Đơn hàng không tồn tại"), status = status.HTTP_200_OK)

        obj = Order.objects.get(pk = id)
        serializer = ResponseOrderSerializer(obj)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)
