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

from management.models import InventoryReceivingVoucher, InventoryVoucher, Supplier, User, WarehouseTransaction, created_updated
from management.serializers.inventory import InventoryRCSerializer, InventoryRecordSerializer, ResponseInventoryRCSerializer, ResponseInventoryRecordSerializer, ResponseWarehouseTransactionSerializer
from management.utils import perms
from management import swagger

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

class InventoryRCView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=InventoryRCSerializer,
        responses={200: swagger.inventory_receiving["get"]})
    def post(self, request):
        serializer = InventoryRCSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        obj = serializer.save()
        created_updated(obj, request)
        response = ResponseInventoryRCSerializer(obj)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return InventoryReceivingVoucher.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.inventory_receiving["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = ResponseInventoryRCSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class InventoryRCIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=InventoryRCSerializer,
        responses={200: swagger.inventory_receiving["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not InventoryReceivingVoucher.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Phiếu nhập hàng không tồn tại"), status = status.HTTP_200_OK)

        voucher = InventoryReceivingVoucher.objects.get(pk = id)
        serializer = InventoryRCSerializer(voucher, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        obj = serializer.save()
        created_updated(obj, request)
        response = ResponseInventoryRCSerializer(obj)

        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.inventory_receiving["get"]})
    @method_permission_classes((perms.IsOwnUserOrAdmin, ))
    def get(self, request, id):
        if not InventoryReceivingVoucher.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Phiếu nhập hàng không tồn tại"), status = status.HTTP_200_OK)

        voucher = InventoryReceivingVoucher.objects.get(pk = id)
        serializer = ResponseInventoryRCSerializer(voucher)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    # @swagger_auto_schema(
    #     manual_parameters=[SwaggerSchema.token],
    #     responses={200: SwaggerSchema.success()})
    # @method_permission_classes((perms.IsAdminUser, ))
    # def delete(self, request, id):
    #     if not InventoryReceivingVoucher.objects.filter(pk = id).exists():
    #         return Response(data = ApiCode.error(message="Phiếu nhập hàng không tồn tại"), status = status.HTTP_200_OK)

    #     voucher = InventoryReceivingVoucher.objects.get(pk = id)

    #     try:
    #         voucher.delete()
    #     except:
    #         return Response(data = ApiCode.error(message="Không thể xóa phiếu nhập hàng này"), status = status.HTTP_200_OK)
    #     return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

##############################################
class InventoryRecordView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=InventoryRecordSerializer,
        responses={200: swagger.inventory_record["get"]})
    def post(self, request):
        serializer = InventoryRecordSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        obj = serializer.save()
        created_updated(obj, request)
        response = ResponseInventoryRecordSerializer(obj)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return InventoryVoucher.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.inventory_record["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = ResponseInventoryRecordSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class InventoryRecordIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=InventoryRecordSerializer,
        responses={200: swagger.inventory_record["get"]})
    @method_permission_classes((perms.IsAdminUser, ))
    def put(self, request, id):
        if not InventoryVoucher.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Phiếu kiểm kê không tồn tại"), status = status.HTTP_200_OK)

        voucher = InventoryVoucher.objects.get(pk = id)
        serializer = InventoryRecordSerializer(voucher, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        obj = serializer.save()
        created_updated(obj, request)
        response = ResponseInventoryRecordSerializer(obj)

        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.inventory_record["get"]})
    @method_permission_classes((perms.IsOwnUserOrAdmin, ))
    def get(self, request, id):
        if not InventoryVoucher.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Phiếu kiểm kê không tồn tại"), status = status.HTTP_200_OK)

        voucher = InventoryVoucher.objects.get(pk = id)
        serializer = ResponseInventoryRecordSerializer(voucher)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

    # @swagger_auto_schema(
    #     manual_parameters=[SwaggerSchema.token],
    #     responses={200: SwaggerSchema.success()})
    # @method_permission_classes((perms.IsAdminUser, ))
    # def delete(self, request, id):
    #     if not InventoryVoucher.objects.filter(pk = id).exists():
    #         return Response(data = ApiCode.error(message="Phiếu kiểm kê không tồn tại"), status = status.HTTP_200_OK)

    #     voucher = InventoryVoucher.objects.get(pk = id)

    #     try:
    #         voucher.delete()
    #     except:
    #         return Response(data = ApiCode.error(message="Không thể xóa phiếu kiểm kê này"), status = status.HTTP_200_OK)
    #     return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


##############################################
class WarehouseTransactionView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return WarehouseTransaction.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.warehouse_transaction["list"]})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = ResponseWarehouseTransactionSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class WarehouseTransactionIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.warehouse_transaction["get"]})
    @method_permission_classes((perms.IsOwnUserOrAdmin, ))
    def get(self, request, id):
        if not WarehouseTransaction.objects.filter(pk = id).exists():
            return Response(data = ApiCode.error(message="Mã biến động kho không tồn tại"), status = status.HTTP_200_OK)

        transaction = WarehouseTransaction.objects.get(pk = id)
        serializer = ResponseWarehouseTransactionSerializer(transaction)
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)