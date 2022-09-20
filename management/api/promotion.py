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

from management.models import CalculationUnit, HierarchyTree, PriceList, Product, ProductGroup, Supplier, User
from management.serializers.product import CalculationUnitSerializer, CategorySerializer, CategoryTreeSerializer, PriceListSerializer, ProductGroupSerializer, ProductSerializer, ReadProductSerializer
from management.serializers.promotion import PromitionSerializer
from management.utils import perms
from management.serializers.user import (
    AddUserSerializer, UpdateUserSerializer, UserSerializer, 
    # ResponseCustomerSerializer, UpdateCustomerSerializer
)
from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.product import  SwaggerProductSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

from management.utils.perms import method_permission_classes
from rest_framework import exceptions

class PromotionView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    # @swagger_auto_schema(
    #     manual_parameters=[SwaggerSchema.token],
    #     request_body=CategorySerializer,
    #     responses={200: swagger.category["get"]})
    def post(self, request):
        serializer = PromitionSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        promotion = serializer.save()
        response = PromitionSerializer(promotion)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

#     def get_queryset(self):
#         return HierarchyTree.objects.filter(type="product", parent=None)

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: swagger.category["get"]})
#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         response = CategoryTreeSerializer(data=queryset, many=True)
#         response.is_valid()
#         return Response(data = ApiCode.success(data={
#             "count": len(response.data),
#             "results": response.data
#         }), status = status.HTTP_200_OK)

# class CategoryIdView(generics.GenericAPIView):
#     authentication_classes = [JWTAuthentication]

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         request_body=CategorySerializer,
#         responses={200: swagger.category["get"]})
#     @method_permission_classes((perms.IsAdminUser, ))
#     def put(self, request, id):
#         if not HierarchyTree.objects.filter(pk = id).exists():
#             return Response(data = ApiCode.error(message="Danh mục sản phẩm không tồn tại"), status = status.HTTP_200_OK)

#         category = HierarchyTree.objects.get(pk = id)
#         serializer = CategorySerializer(category, data=request.data)

#         if serializer.is_valid() == False:
#             return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

#         catergory = serializer.save()
#         response = CategoryTreeSerializer(catergory)

#         return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: swagger.category["get"]})
#     @method_permission_classes((perms.IsAdminUser, ))
#     def get(self, request, id):
#         if not HierarchyTree.objects.filter(pk = id).exists():
#             return Response(data = ApiCode.error(message="Danh mục sản phẩm không tồn tại"), status = status.HTTP_200_OK)

#         category = HierarchyTree.objects.get(pk = id)
#         serializer = CategoryTreeSerializer(category)
#         return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: SwaggerSchema.success()})
#     @method_permission_classes((perms.IsAdminUser, ))
#     def delete(self, request, id):
#         if not HierarchyTree.objects.filter(pk = id).exists():
#             return Response(data = ApiCode.error(message="Danh mục sản phẩm không tồn tại"), status = status.HTTP_200_OK)

#         category = HierarchyTree.objects.get(pk = id)

#         try:
#             category.delete()
#         except:
#             return Response(data = ApiCode.error(message="Không thể xóa danh mục sản phẩm này"), status = status.HTTP_200_OK)
#         return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
