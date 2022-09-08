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

from management.models import User
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

class UserView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=AddUserSerializer,
        responses={200: SwaggerUserSchema.customer_info()})
    def post(self, request):
        if(resolve(request.get_full_path()).url_name == "staff"):
            if not request.user.is_superuser:
                raise exceptions.PermissionDenied


        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        if User.objects.filter(phone=serializer.validated_data["phone"]).exists():
            return Response(data = ApiCode.error(message="Số điện thoại bị trùng"), status = status.HTTP_200_OK)

        user = serializer.save()
        if(resolve(request.get_full_path()).url_name == "staff"):
            user.is_staff = True
            user.save()

        response = UserSerializer(user)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    def get_queryset(self):
        return User.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_list})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if(resolve(request.get_full_path()).url_name == "customer"):
            queryset = queryset.filter(is_staff=False).filter(is_superuser=False)
        else:
            queryset = queryset.filter(is_staff=True)

        response = UserSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class UserIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        request_body=UpdateUserSerializer,
        responses={200: SwaggerUserSchema.customer_info()})
    @method_permission_classes((permissions.IsAdminUser, ))
    def put(self, request, id):
        if(resolve(request.get_full_path()).url_name == "staff_id"):
            if not request.user.is_superuser:
                raise exceptions.PermissionDenied

        user = get_object_or_404(User, id=id)
        serializer = UpdateUserSerializer(user, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        user = serializer.save()

        response = UserSerializer(user)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_info()})
    @method_permission_classes((perms.IsOwnUserOrAdmin, ))
    def get(self, request, id):
        if not User.objects.filter(id=id).exists():
            return Response(data = ApiCode.error(message="Không tồn tại người dùng này"), status = status.HTTP_200_OK)

        customer = User.objects.get(id=id)
        response = UserSerializer(customer)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})
    @method_permission_classes((permissions.IsAdminUser, ))
    def delete(self, request, id):
        if(resolve(request.get_full_path()).url_name == "staff_id"):
            if not request.user.is_superuser:
                raise exceptions.PermissionDenied
                
        if not User.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        user = User.objects.get(pk=id)
        try:
            user.delete()
        except:
            return Response(data = ApiCode.error(message="Không thể xóa người dùng này"), status = status.HTTP_200_OK)
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
