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

from management.models import CalculationUnit, HierarchyTree, PriceList, Product, ProductGroup, Supplier, User, created_updated
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

class ProductGroupView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=ProductGroupSerializer,
        responses={200: swagger.product_group["get"]})
    def post(self, request):
        serializer = ProductGroupSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        obj = serializer.save()
        created_updated(obj, request)
        
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return ProductGroup.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.product_group["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = ProductGroupSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class ProductGroupIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=ProductGroupSerializer,
        responses={200: swagger.product_group["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not ProductGroup.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Nhóm sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        product_group = ProductGroup.objects.get(pk = id)
        serializer = ProductGroupSerializer(product_group, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        obj = serializer.save()
        created_updated(obj, request)

        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.product_group["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not ProductGroup.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Nhóm sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        product_group = ProductGroup.objects.get(pk = id)
        serializer = ProductGroupSerializer(product_group)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not ProductGroup.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Nhóm sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        product_group = ProductGroup.objects.get(pk = id)

        try:
            product_group.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa nhóm sản phẩm này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


class CalculationUnitView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=CalculationUnitSerializer,
        responses={200: swagger.unit["get"]})
    def post(self, request):
        serializer = CalculationUnitSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        obj = serializer.save()
        created_updated(obj, request)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return CalculationUnit.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.unit["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = CalculationUnitSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class CalculationUnitIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=CalculationUnitSerializer,
        responses={200: swagger.unit["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not CalculationUnit.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Đơn vị tính không tồn tại"), status = status.HTTP_200_OK)

        unit = CalculationUnit.objects.get(pk = id)
        serializer = CalculationUnitSerializer(unit, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        serializer.save()
        created_updated(unit, request)

        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.unit["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not CalculationUnit.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Đơn vị tính không tồn tại"), status = status.HTTP_200_OK)

        unit = CalculationUnit.objects.get(pk = id)
        serializer = CalculationUnitSerializer(unit)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not CalculationUnit.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Đơn vị tính không tồn tại"), status = status.HTTP_200_OK)

        unit = CalculationUnit.objects.get(pk = id)

        try:
            unit.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa đơn vị tính này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


class ProductView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=ProductSerializer,
        responses={200: swagger.product["get"]})
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        product = serializer.save()
        created_updated(product, request)
        response = ReadProductSerializer(product)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return Product.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        query_serializer=SellableSerializer,
        responses={200: swagger.product["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        sellable = request.query_params.get('sellable')
        if sellable:
            queryset = queryset.filter(status=True)
            queryset = [x for x in queryset if x._have_price()]
            
        response = ReadProductSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class ProductIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=ProductSerializer,
        responses={200: swagger.product["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not Product.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        product = Product.objects.get(pk = id)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        product = serializer.save()
        created_updated(product, request)
        response = ReadProductSerializer(product)

        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.product["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not Product.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        product = Product.objects.get(pk = id)
        serializer = ReadProductSerializer(product)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not Product.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        product = Product.objects.get(pk = id)

        try:
            product.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa sản phẩm này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


class PriceListView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=PriceListSerializer,
        responses={200: swagger.pricelist["get"]})
    def post(self, request):
        serializer = PriceListSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        obj = serializer.save()
        created_updated(obj, request)
        response = ResponsePriceListSerializer(obj)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return PriceList.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.pricelist["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = ResponsePriceListSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class PriceListIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=PriceListSerializer,
        responses={200: swagger.pricelist["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not PriceList.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Bảng giá không tồn tại"), status = status.HTTP_200_OK)

        pricelist = PriceList.objects.get(pk = id)
        serializer = PriceListSerializer(pricelist, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        obj = serializer.save()
        created_updated(obj, request)
        response = ResponsePriceListSerializer(obj)

        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.pricelist["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not PriceList.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Bảng giá không tồn tại"), status = status.HTTP_200_OK)

        pricelist = PriceList.objects.get(pk = id)
        serializer = ResponsePriceListSerializer(pricelist)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not PriceList.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Bảng giá không tồn tại"), status = status.HTTP_200_OK)

        pricelist = PriceList.objects.get(pk = id)

        try:
            pricelist.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa bảng giá này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

###############################

class CategoryView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=CategorySerializer,
        responses={200: swagger.category["get"]})
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        product = serializer.save()
        created_updated(product, request)
        response = CategorySerializer(product)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return HierarchyTree.objects.filter(type="product", parent=None)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.category["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = CategoryTreeSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class CategoryIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=CategorySerializer,
        responses={200: swagger.category["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not HierarchyTree.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Danh mục sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        category = HierarchyTree.objects.get(pk = id)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        catergory = serializer.save()
        created_updated(catergory, request)
        response = CategoryTreeSerializer(catergory)

        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.category["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not HierarchyTree.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Danh mục sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        category = HierarchyTree.objects.get(pk = id)
        serializer = CategoryTreeSerializer(category)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((perms.IsAdminUser, ))
    def delete(self, request, id):
        if not HierarchyTree.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Danh mục sản phẩm không tồn tại"), status = status.HTTP_200_OK)

        category = HierarchyTree.objects.get(pk = id)

        try:
            category.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa danh mục sản phẩm này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


# 

class CategoryToSelectView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return HierarchyTree.objects.filter(type="product", parent=None)

    # @swagger_auto_schema(
    #     manual_parameters=[SwaggerSchema.token],
    #     responses={200: swagger.category["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = CategoryTreeSelectSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

        
class CategoryToParentView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get(self, request, id):

        curent = HierarchyTree.objects.get(pk = id)
        data = []
        while(curent):
            print(curent)
            data.insert(0, curent.id)
            curent = curent.parent

        return Response(data = ApiCode.success(data={
            "tree": data
        }), status = status.HTTP_200_OK)