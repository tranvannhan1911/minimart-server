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

from management.models import CalculationUnit, HierarchyTree, Order, OrderDetail, OrderRefund, PriceDetail, PriceList, Product, ProductGroup, Promotion, PromotionLine, Supplier, UnitExchange, User, created_updated
from management.serializers.product import CalculationUnitSerializer, CategorySerializer, CategoryTreeSerializer, PriceListSerializer, ProductGroupSerializer, ProductSerializer, ReadProductSerializer
from management.serializers.promotion import PromitionSerializer, PromotionLineSerializer
from management.serializers.sell import OrderRefundSerializer, OrderSerializer, ResponseOrderRefundSerializer, ResponseOrderSerializer
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
        
        for detail in request.data["details"]:
            pricedetail = PriceDetail.objects.get(pk=detail["price"])
            unit_exchange = UnitExchange.objects.get(pk=detail["unit_exchange"])
            product = Product.objects.get(pk=detail["product"])
            quantity = detail["quantity"]*unit_exchange.value
            stock = product.stock()
            if stock < quantity:
                return Response(
                    data = ApiCode.error(message="Sản phẩm "+product.name+" chỉ còn "+product.remain()), 
                    status = status.HTTP_200_OK)

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
        request_body=OrderSerializer,
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

##########################

class OrderRefundView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=OrderRefundSerializer,
        responses={200: swagger.refund["get"]})
    def post(self, request):
        serializer = OrderRefundSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        obj = serializer.save()
        created_updated(obj, request)
        response = ResponseOrderRefundSerializer(obj)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return OrderRefund.objects.filter()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.refund["get"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = ResponseOrderRefundSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class OrderRefundIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=OrderRefundSerializer,
        responses={200: swagger.refund["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not OrderRefund.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Đơn hủy không tồn tại"), status = status.HTTP_200_OK)

        obj = OrderRefund.objects.get(pk = id)
        serializer = OrderRefundSerializer(obj, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        obj = serializer.save()
        created_updated(obj, request)
        response = ResponseOrderRefundSerializer(obj)

        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.refund["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not OrderRefund.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Đơn hủy không tồn tại"), status = status.HTTP_200_OK)

        obj = OrderRefund.objects.get(pk = id)
        serializer = ResponseOrderRefundSerializer(obj)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)
