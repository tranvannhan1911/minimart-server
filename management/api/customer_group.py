
from pprint import pprint
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from management.models import CustomerGroup
from management.serializers.user import CustomerGroupSerializer
from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.user import  SwaggerUserSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

class AddCustomerGroupView(generics.GenericAPIView):
    serializer_class = CustomerGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_group_get})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
        customer_group = serializer.save()
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

class UpdateCustomerGroupView(generics.GenericAPIView):
    serializer_class = CustomerGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_group_get})
        
    def put(self, request, id):
        if not CustomerGroup.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer_group = CustomerGroup.objects.get(pk=id)
        serializer = self.get_serializer(customer_group, data=request.data)

        if serializer.is_valid() == False:
            return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

        serializer.save()
        return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

class GetCustomerGroupView(generics.RetrieveAPIView):
    # serializer_class = CustomerGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_group_get})
    def get(self, request, id):
        if not CustomerGroup.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer_group = CustomerGroup.objects.get(pk=id)
        response = CustomerGroupSerializer(customer_group)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

class ListCustomerGroupView(generics.GenericAPIView):
    serializer_class = CustomerGroupSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return CustomerGroup.objects.all()

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerUserSchema.customer_group_list})
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response = self.get_serializer(data=queryset, many=True)
        response.is_valid()
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)


class DeleteCustomerGroupView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (permissions.IsAdminUser,)

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: SwaggerSchema.success()})

    def delete(self, request, id):
        if not CustomerGroup.objects.filter(pk=id).exists():
            return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

        customer_group = CustomerGroup.objects.get(pk=id)
        customer_group.delete()
        return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

