from rest_framework import serializers
from rest_framework_simplejwt import serializers as serializers_jwt
from management.models import Customer, User
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

class ReadCustomerSerializer(serializers.HyperlinkedModelSerializer):
    phone = serializers.CharField(source='account.phone')
    class Meta:
        model = Customer
        fields = ('customer_id', 'type', 'fullname', 'gender', 'note', 'phone')

class ResponseCustomerSerializer(ResponeSerializer):
    data = ReadCustomerSerializer()