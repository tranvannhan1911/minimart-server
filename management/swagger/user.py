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
                        "id": 3,
                        "customer_group": [
                            {
                                "id": 1,
                                "name": "Khách hàng mới",
                                "description": "Khách hàng mới",
                                "note": "Không"
                            }
                        ],
                        "last_login": None,
                        "is_superuser": False,
                        "is_staff": False,
                        "is_active": True,
                        "date_joined": "2022-09-08T14:20:01.799695Z",
                        "phone": "0987654343",
                        "fullname": "Trần Văn Nhânnn",
                        "gender": "M",
                        "address": None,
                        "note": "h",
                        "groups": [],
                        "user_permissions": []
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
                            "id": 3,
                            "customer_group": [
                                {
                                    "id": 1,
                                    "name": "Khách hàng mới",
                                    "description": "Khách hàng mới",
                                    "note": "Không"
                                }
                            ],
                            "last_login": None,
                            "is_superuser": False,
                            "is_staff": False,
                            "is_active": True,
                            "date_joined": "2022-09-08T14:20:01.799695Z",
                            "phone": "0987654343",
                            "fullname": "Trần Văn Nhânnn",
                            "gender": "M",
                            "address": None,
                            "note": "h",
                            "groups": [],
                            "user_permissions": []
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
                    "id": 3,
                    "customer_group": [],
                    "last_login": None,
                    "is_superuser": False,
                    "is_staff": True,
                    "is_active": True,
                    "date_joined": "2022-09-08T14:20:01.799695Z",
                    "phone": "0987654343",
                    "fullname": "Trần Văn Nhânnn",
                    "gender": "M",
                    "address": None,
                    "note": "h",
                    "groups": [],
                    "user_permissions": []
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
                        "id": 3,
                        "customer_group": [],
                        "last_login": None,
                        "is_superuser": False,
                        "is_staff": True,
                        "is_active": True,
                        "date_joined": "2022-09-08T14:20:01.799695Z",
                        "phone": "0987654343",
                        "fullname": "Trần Văn Nhânnn",
                        "gender": "M",
                        "address": None,
                        "note": "h",
                        "groups": [],
                        "user_permissions": []
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
                    "id": 1,
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
                        "id": 1,
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