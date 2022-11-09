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

class MobileProductView(generics.GenericAPIView):
    @swagger_auto_schema(
        responses={200: swagger.product["get"]})
    def get(self, request, barcode):
        if not Product.objects.filter(barcode = barcode).exists():
            return Response(data = ApiCode.error(message="Sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        product = Product.objects.get(barcode = barcode)
        serializer = ReadProductSerializer(product)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)
