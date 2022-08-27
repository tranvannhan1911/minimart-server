from rest_framework import serializers
from rest_framework_simplejwt import serializers as serializers_jwt
from management.models import Customer, CustomerGroup, User
from management.serializers import ResponeSerializer

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()

class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    new_password = serializers.CharField()

class CustomerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='account.phone')
    class Meta:
        model = Customer
        fields = ('customer_id', 'type', 'fullname', 'gender', 'note', 'phone')
        extra_kwargs = {
            'customer_id': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        account = User.objects.create(phone=validated_data["account"]["phone"])
        validated_data.pop("account")
        customer = Customer.objects.create(
            account=account,
            **validated_data
        )
        return customer

class UpdateCustomerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='account.phone')
    class Meta:
        model = Customer
        fields = ('type', 'fullname', 'gender', 'note', 'phone')
        extra_kwargs = {
            'type': {
                'required': True
            },
            'fullname': {
                'required': True
            },
            'gender': {
                'required': True
            },
            'note': {
                'required': True
            },
            'phone': {
                'required': True
            },
        }

    def update(self, instance, validated_data):
        account = User.objects.get(phone=validated_data["account"]["phone"])
        # instance.account = account
        instance.type = validated_data["type"]
        instance.fullname = validated_data["fullname"]
        instance.gender = validated_data["gender"]
        instance.note = validated_data["note"]
        instance.save()
        return instance


class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = ('id', 'name', 'description', 'note')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }


############# response ################
class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class ResponseTokenSerializer(ResponeSerializer):
    data = TokenSerializer()

class TokenAccessSerializer(serializers.Serializer):
    access = serializers.CharField()

class ResponseTokenAccessSerializer(ResponeSerializer):
    data = TokenAccessSerializer()

class ReadCustomerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='account.phone')
    class Meta:
        model = Customer
        fields = ('customer_id', 'type', 'fullname', 'gender', 'note', 'phone')

class ResponseCustomerSerializer(ResponeSerializer):
    data = ReadCustomerSerializer()