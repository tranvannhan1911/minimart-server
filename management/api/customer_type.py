
from pprint import pprint
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from management.models import CustomerType
from management.serializers.user import CustomerTypeSerializer
from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.user import  SwaggerUserSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

class AddCustomerTypeView(generics.GenericAPIView):
    serializer_class = CustomerTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_type_get})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        customer_type = serializer.save()
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

class UpdateCustomerTypeView(generics.GenericAPIView):
    serializer_class = CustomerTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_type_get})
        
    def put(self, request, id):
        if not CustomerType.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer_type = CustomerType.objects.get(pk=id)
        serializer = self.get_serializer(customer_type, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        serializer.save()
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

class GetCustomerTypeView(generics.RetrieveAPIView):
    # serializer_class = CustomerTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_type_get})
    def get(self, request, id):
        if not CustomerType.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer_type = CustomerType.objects.get(pk=id)
        response = CustomerTypeSerializer(customer_type)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

class ListCustomerTypeView(generics.GenericAPIView):
    serializer_class = CustomerTypeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return CustomerType.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_type_list})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = self.get_serializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)


class DeleteCustomerTypeView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})

    def delete(self, request, id):
        if not CustomerType.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer_type = CustomerType.objects.get(pk=id)
        customer_type.delete()
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

