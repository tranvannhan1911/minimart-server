from rest_framework import serializers
from rest_framework_simplejwt import serializers as serializers_jwt
from management.models import Customer, CustomerGroup, User
from management.serializers import ResponeSerializer
from management.serializers.address import CityDistricWardSerializer

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()

class PhoneVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField()
    new_password = serializers.CharField()



class CustomerGroupSerializer(serializers.ModelSerializer):
    # user_created = UserSerializer(read_only=True)
    # user_updated = UserSerializer(read_only=True)
    class Meta:
        model = CustomerGroup
        fields = '__all__'
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }
        
class UserSerializer(serializers.ModelSerializer):
    customer_group = CustomerGroupSerializer(read_only=True, many=True)
    class Meta:
        model = User
        exclude = ('password', )
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

class AddUserSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('fullname', 'gender', 'note', 'phone', 'address', 'date_created', 'is_manager',
            'user_created', 'user_updated', 'ward')
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
        extra_kwargs = {
            'fullname': {
                'required': True
            },
            'phone': {
                'required': True
            }
        }

class UpdateUserSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('fullname', 'gender', 'note', 'address', 'date_created', 'is_manager',
            'user_created', 'user_updated', 'ward')
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')
        extra_kwargs = {
            'fullname': {
                'required': True
            }
        }


class AccountSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = User
        exclude = ('password', )
        read_only_fields = ('date_created', 'user_created', 
            'date_updated', 'user_updated')

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


##########################

class CustomerSerializer(serializers.ModelSerializer):
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        exclude = ('password', )
        read_only_fields = ('last_login', 'date_created', 'user_created', 
            'date_updated', 'user_updated')
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
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    class Meta:
        model = Customer
        exclude = ('password', )


class ResponseCustomerWardSerializer(serializers.ModelSerializer):
    customer_group = CustomerGroupSerializer(read_only=True, many=True)
    user_created = UserSerializer(read_only=True)
    user_updated = UserSerializer(read_only=True)
    ward = CityDistricWardSerializer()
    class Meta:
        model = Customer
        exclude = ('password', )