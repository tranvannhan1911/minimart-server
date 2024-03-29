import json
from secrets import choice
from drf_yasg import openapi
from management.serializers import ResponeSuccessSerializer
from management.utils.apicode import ApiCode
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class SwaggerSchema():

    token = openapi.Parameter("Authorization", in_=openapi.IN_HEADER, type=openapi.TYPE_STRING, required=True)
    start_date = openapi.Parameter("start_date", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
    end_date = openapi.Parameter("end_date", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False)
    staff_id = openapi.Parameter("staff_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False)
    customer_id = openapi.Parameter("customer_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False)
    promotion_type = openapi.Parameter("type", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False, description="Order: chiết khấu hoặc giảm tiền, Product: Tặng sản phẩm")
    product_id = openapi.Parameter("product_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False)
    product_group_id = openapi.Parameter("product_group_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False)
    product_category_id = openapi.Parameter("product_category_id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False)
    date_required = openapi.Parameter("date", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True)

    @staticmethod
    def success():
        return openapi.Response(
            description="Successful",
            schema=ResponeSuccessSerializer,
            examples={
                "application/json": ApiCode.success()
            }
        )

def get_example(name):
    f = open(dir_path+'/examples/'+name+'.json')
    data = json.load(f)
    # print(data)
    return {
        "get": openapi.Response(
                description="Successful",
                examples={
                    "application/json": ApiCode.success(data=data)
                    }),
        "list": openapi.Response(
                description="Successful",
                examples={
                    "application/json": ApiCode.success_list(lst=[data])
                    }),
    }
    

token = openapi.Response(
    description="Successful",
    examples={
        "application/json": ApiCode.success(data={
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwicGhvbmUiOiIwMzY5NDYyMzA4In0.h1V-mVuoJgWQuPJzrx-miA6mo_f8QECSE8f1UCHxzY0",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcwMTA0NTE2LCJpYXQiOjE2Njc1MTI1MTYsImp0aSI6ImM5MmZjOTY5NzNlYTRiNWM5NzhjYTUyNTVmOTBiOWY2IiwiaWQiOjYsInBob25lIjoiMDM2OTQ2MjMwOCJ9.NMOIQgi9ZHWp_T4EbpLFHdKgRgs_YbXJcNGoC8QIi9M"
        })
    })

customer = get_example("customer")
category = get_example("category")
inventory_receiving = get_example("inventory_receiving")
inventory_record = get_example("inventory_record")
warehouse_transaction = get_example("warehouse_transaction")
promotion_line = get_example("promotion_line")
promotion = get_example("promotion")
product = get_example("product")
product_group = get_example("product_group")
unit = get_example("unit")
pricelist = get_example("pricelist")
order = get_example("order")
refund = get_example("refund")
promotion_history = get_example("promotion_history")
statistic_sales_staff = get_example("statistic_sales_staff")
statistic_sales_customer = get_example("statistic_sales_customer")
statistic_refund = get_example("statistic_refund")
statistic_promotion = get_example("statistic_promotion")
statistic_inventory_receiving = get_example("statistic_inventory_receiving")
statistic_stock = get_example("statistic_stock")
statistic_dashboard = get_example("statistic_dashboard")


