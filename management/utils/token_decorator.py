import pprint
from rest_framework.response import Response
from rest_framework import status
from management.utils.apicode import ApiCode
from management.models import Customer
import jwt
from supermarket.settings import SECRET_KEY
from datetime import datetime

def token_required(func):
    def inner(request, *args, **kwargs):
        try:
            if "HTTP_AUTHORIZATION" not in request.request.META.keys():
                return Response(data = ApiCode.error(message="Không tìm thấy token"), status = status.HTTP_401_UNAUTHORIZED)

            token = request.request.META["HTTP_AUTHORIZATION"]
            if not token.startswith("Bearer "):
                return Response(data = ApiCode.error(message="Token không hợp lệ"), status = status.HTTP_401_UNAUTHORIZED)
            
            token = token[7:]
            decode = jwt.decode(token, SECRET_KEY, "HS256")

            exp = datetime.fromtimestamp(decode["exp"])
            if exp < datetime.now() or decode["token_type"] != "access":
                return Response(data = ApiCode.error(message="Token không hợp lệ"), status = status.HTTP_401_UNAUTHORIZED)

            if not Customer.objects.filter(pk=decode["id"]).exists():
                return Response(data = ApiCode.error(message="Token không hợp lệ"), status = status.HTTP_401_UNAUTHORIZED)
            
            request.request.customer = Customer.objects.get(pk=decode["id"])
        except:
            return Response(data = ApiCode.error(message="Token không hợp lệ"), status = status.HTTP_401_UNAUTHORIZED)
            
        return func(request, *args, **kwargs)
    return inner