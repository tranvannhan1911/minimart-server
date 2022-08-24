from drf_yasg import openapi
from management.serializers import ResponeSuccessSerializer
from management.utils.apicode import ApiCode
class SwaggerSchema():
    @staticmethod
    def success():
        return openapi.Response(
            description="Successful",
            schema=ResponeSuccessSerializer,
            examples={
                "application/json": ApiCode.success()
            }
        )