from datetime import datetime
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
from django.utils import timezone

from management.models import CalculationUnit, HierarchyTree, PriceDetail, PriceList, Product, ProductGroup, Supplier, User, created_updated
from management.serializers.product import CalculationUnitSerializer, CategorySerializer, CategoryTreeSelectSerializer, CategoryTreeSerializer, PriceListSerializer, ProductGroupSerializer, ProductSerializer, ReadProductSerializer, ResponsePriceListSerializer, SellableSerializer
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
from management.models import PromotionLine
from management.utils.token_decorator import token_required
from management.serializers.promotion import ResponsePromotionLineSerializer
 
class MobilePromotionPersonalView(generics.GenericAPIView):
    def get_queryset(self):
        return PromotionLine.objects.filter(status=True)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_line["list"]})
    @token_required
    def get(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(
            start_date__lte=timezone.now(),
            start_date__gte=timezone.now()
        ).exclude(promotion__applicable_customer_groups = None)
        queryset = PromotionLine.filter_customer(queryset, request.customer)
        response = ResponsePromotionLineSerializer(many=True)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)
    
class MobilePromotionProductView(generics.GenericAPIView):
    def get_queryset(self):
        return PromotionLine.objects.filter(status=True)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_line["list"]})
    @token_required
    def get(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(
            start_date__lte=timezone.now(),
            start_date__gte=timezone.now(),
            type="Product"
        )
        queryset = PromotionLine.filter_customer(queryset, request.customer)
        response = ResponsePromotionLineSerializer(many=True)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)


class MobilePromotionOrderView(generics.GenericAPIView):
    def get_queryset(self):
        return PromotionLine.objects.filter(status=True)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_line["list"]})
    @token_required
    def get(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(
            start_date__lte=timezone.now(),
            start_date__gte=timezone.now(),
        ).exclude(type="Product")
        queryset = PromotionLine.filter_customer(queryset, request.customer)
        response = ResponsePromotionLineSerializer(many=True)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)
