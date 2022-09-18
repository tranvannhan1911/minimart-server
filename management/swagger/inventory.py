from drf_yasg import openapi
from management.serializers import ResponeSuccessSerializer
from management.utils.apicode import ApiCode

class SwaggerInventorySchema():
    inventory_receiving_get = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "id": 6,
                    "details": [
                        {
                            "id": 7,
                            "unit_exchange": {
                                "id": 1,
                                "unit_name": "Thùng",
                                "value": 24,
                                "allow_sale": True,
                                "unit": 2
                            },
                            "product": {
                                "id": 1,
                                "product_groups": [],
                                "units": [
                                    {
                                        "id": 1,
                                        "unit_name": "Thùng",
                                        "value": 24,
                                        "allow_sale": True,
                                        "unit": 2
                                    }
                                ],
                                "product_code": "BIA333",
                                "name": "Bia 333",
                                "description": None,
                                "image": None,
                                "barcode": "8491992901299",
                                "product_category": None,
                                "base_unit": 1
                            },
                            "quantity": 20,
                            "price": 10000.0,
                            "note": "string"
                        }
                    ],
                    "supplier": {
                        "id": 1,
                        "name": "Aeon Gò Vấp",
                        "phone": "0987654321",
                        "email": None,
                        "address": None,
                        "note": None
                    },
                    "status": "pending",
                    "note": "Đang chờ giao hàng",
                    "total": 200000.0
                }
            }
        }
    )

    inventory_receiving_list = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "count": 1,
                    "results": [
                        {
                        "id": 6,
                        "details": [
                            {
                                "id": 7,
                                "unit_exchange": {
                                    "id": 1,
                                    "unit_name": "Thùng",
                                    "value": 24,
                                    "allow_sale": True,
                                    "unit": 2
                                },
                                "product": {
                                    "id": 1,
                                    "product_groups": [],
                                    "units": [
                                        {
                                            "id": 1,
                                            "unit_name": "Thùng",
                                            "value": 24,
                                            "allow_sale": True,
                                            "unit": 2
                                        }
                                    ],
                                    "product_code": "BIA333",
                                    "name": "Bia 333",
                                    "description": None,
                                    "image": None,
                                    "barcode": "8491992901299",
                                    "product_category": None,
                                    "base_unit": 1
                                },
                                "quantity": 20,
                                "price": 10000.0,
                                "note": "string"
                            }
                        ],
                        "supplier": {
                            "id": 1,
                            "name": "Aeon Gò Vấp",
                            "phone": "0987654321",
                            "email": None,
                            "address": None,
                            "note": None
                        },
                        "status": "pending",
                        "note": "Đang chờ giao hàng",
                        "total": 200000.0
                    }
                    ]
                }
            
            }
        }
    )
