from drf_yasg import openapi
from management.serializers import ResponeSuccessSerializer
from management.utils.apicode import ApiCode

class SwaggerUserSchema():

    @staticmethod
    def customer_info():
        return openapi.Response(
            description="Successful",
            examples={
                "application/json": {
                    "code": 1,
                    "message": "success",
                    "data": {
                        "customer_id": 55,
                        "customer_group": [
                            {
                                "id": 3,
                                "name": "Khách hàng thân thiết",
                                "description": "Khách hàng thân thiết",
                                "note": "string"
                            }
                        ],
                        "fullname": "Lê Dương",
                        "gender": "M",
                        "note": "",
                        "phone": "0987654342"
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
                            "customer_id": 55,
                            "customer_group": [
                                {
                                    "id": 3,
                                    "name": "Khách hàng thân thiết",
                                    "description": "Khách hàng thân thiết",
                                    "note": "string"
                                }
                            ],
                            "fullname": "Lê Dương",
                            "gender": "M",
                            "note": "",
                            "phone": "0987654342"
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

    staff_get = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "staff_id": 1,
                    "phone": "0987654321",
                    "fullname": "Nhân Trần",
                    "cccd": "128912812892",
                    "address": "Thủ Đức",
                    "gender": "M",
                    "day_of_birth": "2001-11-19",
                    "email": "tranvannhan1911@gmail.com",
                    "status": True
                }
            }
        }
    )

    staff_list = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "count": 1,
                    "results": [
                    {
                        "staff_id": 1,
                        "phone": "0987654321",
                        "fullname": "Nhân Trần",
                        "cccd": "128912812892",
                        "address": "Thủ Đức",
                        "gender": "M",
                        "day_of_birth": "2001-11-19",
                        "email": "tranvannhan1911@gmail.com",
                        "status": True
                    }
                    ]
                }
            
            }
        }
    )

    customer_group_get = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "id": 2,
                    "name": "Khách hàng mới",
                    "description": "Khách hàng mới",
                    "note": ""
                }
            }
        }
    )

    customer_group_list = openapi.Response(
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
                        "name": "Khách hàng mới",
                        "description": "Khách hàng mới",
                        "note": ""
                    }
                    ]
                }
            
            }
        }
    )

    get_info_account = openapi.Response(
        description="Successful",
        examples={
            "application/json": {
                "code": 1,
                "message": "success",
                "data": {
                    "id": 2,
                    "last_login": None,
                    "is_superuser": True,
                    "is_staff": True,
                    "is_active": True,
                    "date_joined": "2022-08-22T18:11:01.223032Z",
                    "phone": "0369462308",
                    "groups": [],
                    "user_permissions": []
                }
            }
        }
    )