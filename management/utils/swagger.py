from drf_yasg import openapi
from management.serializers import ResponeSuccessSerializer
from management.utils.apicode import ApiCode
class SwaggerSchema():

    token = openapi.Parameter("Authorization", in_="header", type="string")

    @staticmethod
    def success():
        return openapi.Response(
            description="Successful",
            schema=ResponeSuccessSerializer,
            examples={
                "application/json": ApiCode.success()
            }
        )

    @staticmethod
    def customer_info():
        return openapi.Response(
            description="Successful",
            examples={
                "application/json": {
                    "code": 1,
                    "message": "success",
                    "data": {
                        "customer_id": 36,
                        "type": 2,
                        "fullname": "Trần Văn Nhân",
                        "gender": "U",
                        "note": "",
                        "phone": "0987654344"
                    }
                }
            }
        )

    customer_list = openapi.Response(
            description="Successful",
            examples={
                "application/json": {
                    "code": 1,
                    "message": "success",
                    "data": {
                        "count": 2,
                        "results": [
                        {
                            "customer_id": 36,
                            "type": None,
                            "fullname": "Trần",
                            "gender": "U",
                            "note": "",
                            "phone": "0987654344"
                        },
                        {
                            "customer_id": 37,
                            "type": None,
                            "fullname": "Nhân",
                            "gender": "M",
                            "note": "",
                            "phone": "0987654321"
                        }
                        ]
                    }
                    }
            }
        )