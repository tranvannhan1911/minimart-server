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

from management.models import CalculationUnit, HierarchyTree, PriceList, Product, ProductGroup, Promotion, PromotionLine, Supplier, User, created_updated
from management.serializers.product import CalculationUnitSerializer, CategorySerializer, CategoryTreeSerializer, PriceListSerializer, ProductGroupSerializer, ProductSerializer, ReadProductSerializer
from management.serializers.promotion import PromitionSerializer, PromotionLineSerializer
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

class PromotionView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=PromitionSerializer,
        responses={200: swagger.promotion["get"]})
    def post(self, request):
        serializer = PromitionSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        obj = serializer.save()
        created_updated(obj, request)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return Promotion.objects.filter()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion["get"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = PromitionSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class PromotionIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=PromitionSerializer,
        responses={200: swagger.promotion["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not Promotion.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Chương trình khuyến mãi không tồn tại"), status = status.HTTP_200_OK)

        promotion = Promotion.objects.get(pk = id)
        serializer = PromitionSerializer(promotion, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        obj = serializer.save()
        created_updated(obj, request)

        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not Promotion.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Chương trình khuyến mãi không tồn tại"), status = status.HTTP_200_OK)

        promotion = Promotion.objects.get(pk = id)
        serializer = PromitionSerializer(promotion)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not Promotion.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Chương trình khuyến mãi không tồn tại"), status = status.HTTP_200_OK)

        promotion = Promotion.objects.get(pk = id)

        try:
            promotion.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa chương trình khuyến mãi này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

###################################

class PromotionLineView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=PromotionLineSerializer,
        responses={200: swagger.promotion_line["get"]})
    def post(self, request):
        serializer = PromotionLineSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        # if serializer.data["type"] == "Product":
        #     if serializer.data["detail"]["applicable_products"]
        # elif serializer.data["type"] == "Percent":
        #     pass
        # elif serializer.data["type"] == "Fixed":
        #     pass
        
        obj = serializer.save()
        created_updated(obj, request)
        created_updated(obj.promotion, request)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return PromotionLine.objects.filter()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_line["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = PromotionLineSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class PromotionLineIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=PromotionLineSerializer,
        responses={200: swagger.promotion_line["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not PromotionLine.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Khuyến mãi không tồn tại"), status = status.HTTP_200_OK)

        object = PromotionLine.objects.get(pk = id)
        serializer = PromotionLineSerializer(object, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        obj = serializer.save()
        created_updated(obj, request)
        created_updated(obj.promotion, request)

        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_line["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not PromotionLine.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Khuyến mãi không tồn tại"), status = status.HTTP_200_OK)

        object = PromotionLine.objects.get(pk = id)
        serializer = PromotionLineSerializer(object)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not PromotionLine.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Khuyến mãi không tồn tại"), status = status.HTTP_200_OK)

        object = PromotionLine.objects.get(pk = id)

        try:
            object.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa khuyến mãi này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
        