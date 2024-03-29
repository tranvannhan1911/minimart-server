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

from management.models import CalculationUnit, Customer, HierarchyTree, PriceList, Product, ProductGroup, Promotion, PromotionHistory, PromotionLine, Supplier, User, created_updated
from management.serializers.product import CalculationUnitSerializer, CategorySerializer, CategoryTreeSerializer, PriceListSerializer, ProductGroupSerializer, ProductSerializer, ReadProductSerializer
from management.serializers.promotion import PromitionByOrderSerializer, PromitionByProductSerializer, PromitionByTypeSerializer, PromitionSerializer, PromotionHistorySerializer, PromotionLineSerializer, ResponsePromotionLineSerializer
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
        response = ResponsePromotionLineSerializer(obj)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return PromotionLine.objects.filter()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_line["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = ResponsePromotionLineSerializer(data=queryset, many=True)
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
        response = ResponsePromotionLineSerializer(obj)

        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_line["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not PromotionLine.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Khuyến mãi không tồn tại"), status = status.HTTP_200_OK)

        object = PromotionLine.objects.get(pk = id)
        serializer = ResponsePromotionLineSerializer(object)
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
        
###
# api promotion product lấy danh sách các khuyến mãi có thể áp dụng 
# cho sản phẩm, không kiểm tra số lượng tồn kho
# - nếu tồn tại user thì 
#       với các Promotion tồn tại applicable_customer_groups
#       bỏ các promotion mà user k được áp dụng
class PromotionProductIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        query_serializer=PromitionByProductSerializer,
        responses={200: swagger.promotion_line["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request):
        product_id = int(request.query_params.get('product_id'))
        customer_id = request.query_params.get('customer_id')
        quantity = int(request.query_params.get('quantity'))
        quantity_in_use = int(request.query_params.get('quantity_in_use', 0))
        if not Product.objects.filter(pk = product_id).exists():
            return Response(data = ApiCode.error(message="Sản phẩm không tồn tại"), status = status.HTTP_200_OK)
        
        product = Product.objects.get(pk = product_id)
        promotion_lines = PromotionLine.get_by_product(product)

        if customer_id:
            if not Customer.objects.filter(pk = customer_id).exists():
                return Response(data = ApiCode.error(message="Khách hàng không tồn tại"), status = status.HTTP_200_OK)
        
            customer = Customer.objects.get(pk = customer_id)
            promotion_lines = PromotionLine.filter_customer(promotion_lines, customer)
            for pl in promotion_lines:
                pl.get_remain_today(customer)
                pl.get_remain_customer(customer)

            promotion_lines = PromotionLine.sort_benefit_product(
                    promotion_lines, product, 
                    quantity, customer, quantity_in_use)
        # else:
        #     promotion_lines = promotion_lines.filter(
        #             promotion__applicable_customer_groups=None)
        
        response = ResponsePromotionLineSerializer(promotion_lines, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)


class PromotionByOrderView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        query_serializer=PromitionByOrderSerializer,
        responses={200: swagger.promotion_line["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request):
        amount = int(request.query_params.get('amount'))
        customer_id = request.query_params.get('customer_id')

        promotion_lines = PromotionLine.get_by_order(amount)
        
        if customer_id:
            if not Customer.objects.filter(pk = customer_id).exists():
                return Response(data = ApiCode.error(message="Khách hàng không tồn tại"), status = status.HTTP_200_OK)
            customer = Customer.objects.get(pk = customer_id)
            promotion_lines = PromotionLine.filter_customer(promotion_lines, customer)

        promotion_lines = PromotionLine.sort_benefit_order(promotion_lines, amount)
        for pl in promotion_lines:
            pl.get_remain_today(customer)
            pl.get_remain_customer(customer)
        response = ResponsePromotionLineSerializer(promotion_lines, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)


class PromotionByTypeView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        query_serializer=PromitionByTypeSerializer,
        responses={200: swagger.promotion_line["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request):
        type = request.query_params.get('type')
        customer_id = request.query_params.get('customer_id')
        amount = int(request.query_params.get('amount', 0))

        promotion_lines = PromotionLine.get_by_type(type)

        if customer_id:
            if not Customer.objects.filter(pk = customer_id).exists():
                return Response(data = ApiCode.error(message="Khách hàng không tồn tại"), status = status.HTTP_200_OK)
            customer = Customer.objects.get(pk = customer_id)
            promotion_lines = PromotionLine.filter_customer(promotion_lines, customer)

            promotion_lines = PromotionLine.sort_benefit_order(promotion_lines, amount)
            for pl in promotion_lines:
                pl.get_remain_today(customer)
                pl.get_remain_customer(customer)
        response = ResponsePromotionLineSerializer(promotion_lines, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)
###################

class PromotionHistoryView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return PromotionHistory.objects.filter().order_by("-id")

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_history["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = PromotionHistorySerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class PromotionHistoryIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.promotion_history["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def get(self, request, id):
        if not PromotionHistory.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Lịch sử sử dụng khuyến mãi không tồn tại"), status = status.HTTP_200_OK)

        object = PromotionHistory.objects.get(pk = id)
        serializer = PromotionHistorySerializer(object)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)
