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

class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fullname', 'gender', 'note', 'phone', 'address', 'date_created')
        read_only_fields = ('date_created', )
        extra_kwargs = {
            'fullname': {
                'required': True
            },
            'phone': {
                'required': True
            }
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('fullname', 'gender', 'note', 'address', 'date_created')
        read_only_fields = ('date_created', )
        extra_kwargs = {
            'fullname': {
                'required': True
            }
        }


class CustomerGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerGroup
        fields = '__all__'
        read_only_fields = ('date_created', )
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )
        read_only_fields = ('date_created', )

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

class UserSerializer(serializers.ModelSerializer):
    customer_group = CustomerGroupSerializer(read_only=True, many=True)
    class Meta:
        model = User
        exclude = ('password', )
        read_only_fields = ('date_created', )

##########################

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('password', )
        read_only_fields = ('date_created', 'last_login')
        extra_kwargs = {
            'fullname': {
                'required': True
            },
            'phone': {
                'required': True
            }
        }


class ResponseCustomerSerializer(serializers.ModelSerializer):
    customer_group = CustomerGroupSerializer(read_only=True, many=True)
    class Meta:
        model = Customer
        exclude = ('password', )