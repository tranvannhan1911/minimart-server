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
    print(dir_path)
    f = open(dir_path+'/examples/'+name+'.json')
    data = json.load(f)
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
    
inventory_receiving = get_example("inventory_receiving")
inventory_record = get_example("inventory_record")
warehouse_transaction = get_example("warehouse_transaction")