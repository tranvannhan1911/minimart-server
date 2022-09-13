from drf_yasg import openapi
from management.serializers import ResponeSuccessSerializer
from management.utils.apicode import ApiCode

class SwaggerProductSchema():
    product_group_get = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "id": 2,
                    "product_group_code": "MIANLIEN",
                    "name": "Mì ăn liền",
                    "description": "Mì ăn liền ăn liền",
                    "note": "Ăn liền"
                }
            }
        }
    )

    product_group_list = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "count": 1,
                    "results": [
                    {
                        "id": 2,
                        "product_group_code": "MIANLIEN",
                        "name": "Mì ăn liền",
                        "description": "Mì ăn liền ăn liền",
                        "note": "Ăn liền"
                    }
                    ]
                }
            
            }
        }
    )

    calculation_unit_get = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "id": 1,
                    "name": "Lon"
                }
            }
        }
    )

    calculation_unit_list = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "count": 1,
                    "results": [
                    {
                        "id": 1,
                        "name": "Lon"
                    }
                    ]
                }
            
            }
        }
    )

    product_get = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "id": 1,
                    "product_code": "BIA333",
                    "name": "Bia 333",
                    "description": None,
                    "image": None,
                    "barcode": "8491992901299",
                    "product_category": None,
                    "base_unit": None,
                    "product_groups": []
                }
            }
        }
    )

    product_list = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "count": 1,
                    "results": [
                    {
                        "id": 1,
                        "product_code": "BIA333",
                        "name": "Bia 333",
                        "description": None,
                        "image": None,
                        "barcode": "8491992901299",
                        "product_category": None,
                        "base_unit": None,
                        "product_groups": []
                    }
                    ]
                }
            
            }
        }
    )