
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from management import swagger

from management.models import Customer, Order, ProductGroup, Supplier, User, created_updated
from management.serializers.statistic import StatisticSalesCustomerSerializer, StatisticSellSerializer
from management.serializers.supplier import SupplierSerializer
from management.utils import perms

from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.user import  SwaggerUserSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

from management.utils.perms import method_permission_classes
from management.utils.utils import to_datetime
from django.db.models import Sum, F, OuterRef, Subquery

class StatisticSellView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return Order.objects.filter(status="complete")

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.statistic_sales_staff["list"]})
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        staff_id = request.query_params.get('staff_id', None)

        queryset = self.get_queryset()
        queryset = Order._filter(queryset, start_date, end_date, staff_id)
        
        queryset = queryset.values('user_created', 'date_created').annotate(
            discount=Sum("total")-Sum("final_total"),
            total=Sum("total"), 
            final_total=Sum("final_total"),
        )
        
        response = []
        for que in queryset.all():
            que["user_created"] = User.objects.get(pk=que["user_created"])
            response.append(que)

        response = StatisticSellSerializer(response, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

        # return Response(data = ApiCode.success(), status = status.HTTP_200_OK)


class StatisticSalesCustomerView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return Order.objects.filter(status="complete")

    @swagger_auto_schema(
        manual_parameters=[SwaggerSchema.token],
        responses={200: swagger.statistic_sales_customer["list"]})
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        customer_id = request.query_params.get('customer_id', None)

        queryset = self.get_queryset()
        queryset = Order._filter_date(queryset, start_date, end_date)
        if customer_id:
            queryset = queryset.filter(customer__id=customer_id)
        
        queryset = queryset.values(
            'customer', 
            'details__product__product_groups', 
            'details__product__product_category'
        ).annotate(
            discount=Sum("total")-Sum("final_total"),
            total=Sum("total"), 
            final_total=Sum("final_total"),
        )
        # print(queryset)

        # return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
        response = []
        for que in queryset.all():
            if que["customer"]:
                que["customer"] = Customer.objects.get(pk=que["customer"])
            else:
                que["customer"] = None

            if que["details__product__product_groups"]:
                que["product_groups"] = ProductGroup.objects.get(pk=que["details__product__product_groups"])
            else:
                que["product_groups"] = None

            if que["details__product__product_category"]:
                que["product_category"] = ProductGroup.objects.get(pk=que["details__product__product_category"])
            else:
                que["product_category"] = None

            del que["details__product__product_groups"]
            del que["details__product__product_category"]
            response.append(que)

        response = StatisticSalesCustomerSerializer(response, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)