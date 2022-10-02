import json
from drf_yasg import openapi
from management.serializers import ResponeSuccessSerializer
from management.utils.apicode import ApiCode
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

class SwaggerSchema():

    token = openapi.Parameter("Authorization", in_="header", type="string", required=True)

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