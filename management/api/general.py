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

from management.models import CounterIndex, Supplier, User, created_updated
from management.serializers.supplier import SupplierSerializer
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


class CounterIndexView(generics.GenericAPIView):
    def get(self, request, table):
        if CounterIndex.objects.filter(table=table).exists():
            return Response(data = ApiCode.success(data={
                "value": CounterIndex.objects.get(table=table).value+1
            }), status = status.HTTP_200_OK)
            
        return Response(data = ApiCode.success(data={
                "value": 1
            }), status = status.HTTP_200_OK)
