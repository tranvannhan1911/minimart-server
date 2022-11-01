
from pprint import pprint
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
import datetime
from management import swagger
from django.db.models.functions import TruncDate

from management.models import Customer, InventoryReceivingVoucher, InventoryReceivingVoucherDetail, Order, OrderRefund, Product, PromotionHistory, PromotionLine, WarehouseTransaction, _filter_date_str, OrderRefundDetail, ProductGroup, Supplier, User, created_updated, filter_product
from management.serializers.statistic import StatisticDashboardSerializer, StatisticInventoryReceivingSerializer, StatisticPromotionHistorySerializer, StatisticRefundSerializer, StatisticSalesCustomerSerializer, StatisticSellSerializer, StatisticStockSerializer
from management.serializers.supplier import SupplierSerializer
from management.utils import perms

from management.utils.apicode import ApiCode
from drf_yasg.utils import swagger_auto_schema

from management.swagger import SwaggerSchema
from management.swagger.user import  SwaggerUserSchema
from rest_framework_simplejwt.authentication import JWTAuthentication

from management.utils.perms import method_permission_classes
from management.utils.utils import end_of_date, start_of_date, to_datetime
from django.db.models import Sum, F, OuterRef, Subquery


class StatisticDashboardView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)


    def top_5_customer(self, start_date, today, user):
        top_5_customer = Order.objects.filter(
                date_created__gte=start_date,
                status="complete",
                user_created=user
            ).values("customer").annotate(
                total=Sum("total"),
                final_total=Sum("final_total"),
            ).order_by("-final_total")[:5]
        
        for elm in top_5_customer:
            elm["customer"] = Customer.objects.filter(pk = int(elm["customer"])).first()

        # print(top_5_customer)
        return top_5_customer

    def top_5_order(self, start_date, today, user):
        top_5_order = Order.objects.filter(
                date_created__gte=start_date,
                user_created=user,
                status="complete"
            ).values("customer").annotate(
                total=Sum("total"),
                final_total=Sum("final_total"),
            ).order_by("-final_total")[:5]
        # print(top_5_order)
        return top_5_order
        
    def order_7_days(self, start_date, today, user):
        order_7_days = Order.objects.filter(
                date_created__gte=start_date,
                user_created=user,
                status="complete"
            )

        res = {}
        delta = datetime.timedelta(days=1)
        while start_date <= today:
            key = start_date.strftime("%d-%m-%Y")
            res[key] = {
                "date": key,
                "total": 0,
                "final_total": 0,
                "count": 0
            }
            start_date += delta

        for elm in order_7_days.all():
            key = elm.date_created.strftime("%d-%m-%Y")
            res[key]["total"] += elm.total
            res[key]["final_total"] += elm.final_total
            res[key]["count"] += 1

        result = []
        for elm in res:
            result.append(res[elm])
            
        return result

    @swagger_auto_schema(
        manual_parameters=[
            SwaggerSchema.token],
        responses={200: swagger.statistic_dashboard["get"]})
    def get(self, request, *args, **kwargs):
        today = end_of_date(timezone.now())
        start_date = start_of_date(today-datetime.timedelta(days=6))
        top_5_customer = self.top_5_customer(start_date, today, request.user)
        top_5_order = self.top_5_order(start_date, today, request.user)
        order_7_days = self.order_7_days(start_date, today, request.user)
        
        count_order_7_days = Order.objects.filter(
            date_created__gte=start_date, 
            user_created=request.user).count()

        count_order_refund_7_days = OrderRefund.objects.filter(
            date_created__gte=start_date, 
            user_created=request.user).count()

        count_customer_7_days = Order.objects.filter(
            date_created__gte=start_date, 
            user_created=request.user).values("customer").count()

        total_money_7_days = Order.objects.filter(
                date_created__gte=start_date,
                status="complete", 
                user_created=request.user
            ).aggregate(Sum("final_total"))["final_total__sum"]
            
        data = {
            "top_5_customer": top_5_customer, 
            "top_5_order": top_5_order,
            "order_7_days": order_7_days, 
            "count_order_7_days": count_order_7_days,
            "count_order_refund_7_days": count_order_refund_7_days, 
            "total_money_7_days": total_money_7_days,
            "count_customer_7_days": count_customer_7_days
        }
        
        response = StatisticDashboardSerializer(data)
        return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

class StatisticSellView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return Order.objects.filter(status="complete")

    @swagger_auto_schema(
        manual_parameters=[
            SwaggerSchema.token, 
            SwaggerSchema.start_date,
            SwaggerSchema.end_date,
            SwaggerSchema.staff_id],
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
            que["user_created"] = User.objects.filter(pk=que["user_created"]).first()
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
        manual_parameters=[
            SwaggerSchema.token, 
            SwaggerSchema.start_date,
            SwaggerSchema.end_date,
            SwaggerSchema.customer_id],
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
                que["customer"] = Customer.objects.filter(pk=que["customer"]).first()
            else:
                que["customer"] = None

            if que["details__product__product_groups"] and ProductGroup.objects.filter(pk=que["details__product__product_groups"]).exists():
                que["product_groups"] = ProductGroup.objects.filter(pk=que["details__product__product_groups"]).first()
            else:
                que["product_groups"] = None

            if que["details__product__product_category"] and ProductGroup.objects.filter(pk=que["details__product__product_category"]).exists():
                que["product_category"] = ProductGroup.objects.filter(pk=que["details__product__product_category"]).first()
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


class StatisticRefundView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return OrderRefundDetail.objects.filter(order_refund__status="complete")

    @swagger_auto_schema(
        manual_parameters=[
            SwaggerSchema.token,
            SwaggerSchema.start_date,
            SwaggerSchema.end_date,
            SwaggerSchema.product_id,
            SwaggerSchema.product_group_id,
            SwaggerSchema.product_category_id],
        responses={200: swagger.statistic_refund["list"]})
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        product_id = request.query_params.get('product_id', None)
        product_group_id = request.query_params.get('product_group_id', None)
        product_category_id = request.query_params.get('product_category_id', None)

        queryset = self.get_queryset()
        queryset = _filter_date_str(queryset, start_date, end_date)
        queryset = filter_product(queryset, product_id, product_group_id, product_category_id)

        response = StatisticRefundSerializer(queryset, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class StatisticPromotionView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return PromotionHistory.objects.filter()

    @swagger_auto_schema(
        manual_parameters=[
            SwaggerSchema.token,
            SwaggerSchema.start_date,
            SwaggerSchema.end_date,
            SwaggerSchema.promotion_type],
        responses={200: swagger.statistic_promotion["list"]})
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        type = request.query_params.get('type', None)

        queryset = self.get_queryset()
        queryset = _filter_date_str(queryset, start_date, end_date)
        queryset = PromotionHistory.filter_type(queryset, type)

        queryset = queryset.values("promotion_line").annotate(
            quantity=Sum("quantity"),
            amount=Sum("amount"),
            type=F("type"),
        )

        for que in queryset:
            que["promotion_line"] = PromotionLine.objects.filter(pk=que["promotion_line"]).first()

        # return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
        response = StatisticPromotionHistorySerializer(queryset, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)


class StatisticInventoryReceivingView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return InventoryReceivingVoucherDetail.objects.filter(receiving_voucher__status="complete")

    @swagger_auto_schema(
        manual_parameters=[
            SwaggerSchema.token,
            SwaggerSchema.start_date,
            SwaggerSchema.end_date,
            SwaggerSchema.product_id,
            SwaggerSchema.product_group_id,
            SwaggerSchema.product_category_id],
        responses={200: swagger.statistic_inventory_receiving["list"]})
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        product_id = request.query_params.get('product_id', None)
        product_group_id = request.query_params.get('product_group_id', None)
        product_category_id = request.query_params.get('product_category_id', None)

        queryset = self.get_queryset()
        queryset = InventoryReceivingVoucherDetail.filter_date(queryset, start_date, end_date)
        queryset = filter_product(queryset, product_id, product_group_id, product_category_id)

        queryset = queryset.values("product").annotate(
            quantity_base_unit=Sum("quantity_base_unit"),
            total=Sum(F("quantity")*F("price"))
        )
        for que in queryset:
            que["product"] = Product.objects.filter(pk=que["product"]).first()
        
        response = StatisticInventoryReceivingSerializer(queryset, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)

class StatisticStockView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = (perms.IsAdminUser,)

    def get_queryset(self):
        return WarehouseTransaction.objects.all()

    @swagger_auto_schema(
        manual_parameters=[
            SwaggerSchema.token,
            SwaggerSchema.date_required,
            SwaggerSchema.product_id,
            SwaggerSchema.product_group_id,
            SwaggerSchema.product_category_id],
        responses={200: swagger.statistic_stock["list"]})
    def get(self, request, *args, **kwargs):
        date = request.query_params.get('date', None)
        product_id = request.query_params.get('product_id', None)
        product_group_id = request.query_params.get('product_group_id', None)
        product_category_id = request.query_params.get('product_category_id', None)
        if not date:
            return Response(data = ApiCode.error(message="Ngày không hợp lệ"), status = status.HTTP_200_OK)
        
        date = to_datetime(date)
        date = end_of_date(date)

        queryset = self.get_queryset()
        queryset = queryset.filter(date_created__lte=date)
        queryset = filter_product(queryset, product_id, product_group_id, product_category_id)

        queryset = queryset.values("product").annotate(
            stock_base_unit=Sum("change")
        )
        for que in queryset:
            que["product"] = Product.objects.filter(pk=que["product"]).first()

        # return Response(data = ApiCode.success(), status = status.HTTP_200_OK)
        response = StatisticStockSerializer(queryset, many=True)
        return Response(data = ApiCode.success(data={
            "count": len(response.data),
            "results": response.data
        }), status = status.HTTP_200_OK)