
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import status

# from management.models import Supplier, created_updated
# from management.serializers.supplier import SupplierSerializer
# from management.utils import perms

# from management.utils.apicode import ApiCode
# from drf_yasg.utils import swagger_auto_schema

# from management.swagger import SwaggerSchema
# from management.swagger.user import  SwaggerUserSchema
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from management.utils.perms import method_permission_classes


# class SupplierIdView(generics.GenericAPIView):
#     authentication_classes = [JWTAuthentication]

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         request_body=SupplierSerializer,
#         responses={200: SwaggerUserSchema.supplier_get})
#     @method_permission_classes((perms.IsAdminUser, ))
#     def put(self, request, id):
#         if not Supplier.objects.filter(pk = id).exists():
#             return Response(data = ApiCode.error(message="Nhà cung cấp không tồn tại"), status = status.HTTP_200_OK)

#         supplier = Supplier.objects.get(pk = id)
#         serializer = SupplierSerializer(supplier, data=request.data)

#         if serializer.is_valid() == False:
#             return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

#         obj = serializer.save()
#         created_updated(obj, request)

#         return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: SwaggerUserSchema.supplier_get})
#     @method_permission_classes((perms.IsOwnUserOrAdmin, ))
#     def get(self, request, id):
#         if not Supplier.objects.filter(pk = id).exists():
#             return Response(data = ApiCode.error(message="Nhà cung cấp không tồn tại"), status = status.HTTP_200_OK)

#         supplier = Supplier.objects.get(pk = id)
#         serializer = SupplierSerializer(supplier)
#         return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)
