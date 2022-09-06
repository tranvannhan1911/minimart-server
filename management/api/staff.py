
# from pprint import pprint
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework import permissions

# from management.models import Customer, Staff
# from management.serializers.staff import StaffSerializer
# from management.utils.apicode import ApiCode
# from drf_yasg.utils import swagger_auto_schema

# from management.swagger import SwaggerSchema
# from management.swagger.user import  SwaggerUserSchema
# from rest_framework_simplejwt.authentication import JWTAuthentication

# class AddStaffView(generics.GenericAPIView):
#     serializer_class = StaffSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = (permissions.IsAdminUser,)

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: SwaggerUserSchema.staff_get})
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid() == False:
#             return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)
        
#         try:
#             staff = serializer.save()
#         except Exception:
#             return Response(data = ApiCode.error(message={"phone": ["duplicated"]}), status = status.HTTP_200_OK)
        
#         return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

# class UpdateStaffView(generics.GenericAPIView):
#     serializer_class = StaffSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = (permissions.IsAdminUser,)

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: SwaggerUserSchema.staff_get})
        
#     def put(self, request, staff_id):
#         if not Staff.objects.filter(staff_id=staff_id).exists():
#             return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

#         staff = Staff.objects.get(staff_id=staff_id)
#         serializer = self.get_serializer(staff, data=request.data)

#         if serializer.is_valid() == False:
#             return Response(data = ApiCode.error(message=serializer.errors), status = status.HTTP_200_OK)

#         staff = serializer.save()
#         return Response(data = ApiCode.success(data=serializer.data), status = status.HTTP_200_OK)

# class GetStaffView(generics.RetrieveAPIView):
#     # serializer_class = StaffSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = (permissions.IsAuthenticated,)

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: SwaggerUserSchema.staff_get})
#     def get(self, request, staff_id):
#         if not Staff.objects.filter(staff_id=staff_id).exists():
#             return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

#         staff = Staff.objects.get(staff_id=staff_id)
#         response = StaffSerializer(staff)
#         return Response(data = ApiCode.success(data=response.data), status = status.HTTP_200_OK)

# class ListStaffView(generics.GenericAPIView):
#     serializer_class = StaffSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         return Staff.objects.all()

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: SwaggerUserSchema.staff_list})
#     def get(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         response = self.get_serializer(data=queryset, many=True)
#         response.is_valid()
#         return Response(data = ApiCode.success(data={
#             "count": len(response.data),
#             "results": response.data
#         }), status = status.HTTP_200_OK)


# class DeleteStaffView(generics.DestroyAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = (permissions.IsAdminUser,)

#     @swagger_auto_schema(
#         manual_parameters=[SwaggerSchema.token],
#         responses={200: SwaggerSchema.success()})

#     def delete(self, request, staff_id):
#         if not Staff.objects.filter(staff_id=staff_id).exists():
#             return Response(data = ApiCode.error(), status = status.HTTP_200_OK)

#         customer = Staff.objects.get(staff_id=staff_id)
#         customer.delete()
#         return Response(data = ApiCode.success(), status = status.HTTP_200_OK)

