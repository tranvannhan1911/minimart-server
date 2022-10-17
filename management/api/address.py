import json
from pprint import pprint
from django.shortcuts import get_object_or_404
from django.urls import resolve
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.forms.models import model_to_dict
from rest_framework import permissions
from vi_address.models import City
from management import serializers

from management.models import Supplier, User, created_updated
from management.serializers.address import AddressSerializer, WardAllSerializer
from management.serializers.supplier import SupplierSerializer
from management.utils import perms

from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.user import  SwaggerUserSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

from vi_address.models import Ward

class AddressView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get(self, request, *args, **kwargs):
        queryset = City.objects.all()
        response = AddressSerializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)


class AddressPathIdView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get(self, request, id):

        curent = Ward.objects.get(pk = id)
        data = [curent.parent_code.parent_code.id, curent.parent_code.id, curent.id]

        return Response(data = ApiCode.success(data={
            "tree": data
        }), status = status.HTTP_200_OK)



class WardView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get(self, request, id):

        ward = Ward.objects.get(pk = id)
        response = WardAllSerializer(ward)

        return Response(data = ApiCode.success(data={
            "ward": response.data
        }), status = status.HTTP_200_OK)