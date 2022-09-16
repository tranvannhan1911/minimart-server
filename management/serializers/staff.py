# from rest_framework import serializers

# from management.models import Staff

# class StaffSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Staff
#         fields = ('staff_id', 'phone', 'fullname', 'cccd', 'address', 'gender', 
#             'day_of_birth', 'email', 'status')
#         extra_kwargs = {
#             'staff_id': {
#                 'read_only': True
#             }
#         }
        

# # class UpdateStaffSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Staff
# #         fields = ('staff_id', 'phone', 'fullname', 'cccd', 'address', 'gender', 
# #             'day_of_birth', 'email', 'status')
# #         extra_kwargs = {
# #             'staff_id': {
# #                 'read_only': True
# #             }
# #         }

# #     def update(self, instance, validated_data):
# #         account = User.objects.get(phone=validated_data["account"]["phone"])
# #         # instance.account = account
# #         instance.type = validated_data["type"]
# #         instance.fullname = validated_data["fullname"]
# #         instance.gender = validated_data["gender"]
# #         instance.note = validated_data["note"]
# #         instance.save()
# #         return instance