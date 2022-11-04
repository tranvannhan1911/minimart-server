
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from management.utils.apicode import ApiCode
from management.utils.token_decorator import token_required
from management.serializers.sell import ResponseOrderSerializer
from management.swagger import SwaggerSchema
from management import swagger
from drf_yasg.utils import swagger_auto_schema

class CustomerOrderView(generics.GenericAPIView):
    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.order["list"]})
    @token_required
    def get(self, request):
        response = ResponseOrderSerializer(request.customer.orders.order_by("-date_created"), many=True)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)
