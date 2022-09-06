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
        fields = ('customer_id', 'customer_group', 'fullname', 'gender', 'note', 'phone', 'address')
        extra_kwargs = {
            'customer_id': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        account = User.objects.create(phone=validated_data["account"]["phone"]) 
        customer_groups = validated_data["customer_group"]
        validated_data.pop("account")
        validated_data.pop("customer_group")
        customer = Customer.objects.create(
            account=account,
            **validated_data
        )
        for cg in customer_groups:
            customer.customer_group.add(cg)
        return customer

class UpdateCustomerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='account.phone')
    class Meta:
        model = Customer
        fields = ('customer_group', 'fullname', 'gender', 'note', 'phone', 'address')
        extra_kwargs = {
            'customer_group': {
                'required': True
            },
            'fullname': {
                'required': True
            }
        }

    def update(self, instance, validated_data):
        # account = User.objects.get(phone=validated_data["account"]["phone"])
        # instance.account = account
        instance.fullname = validated_data["fullname"]
        instance.gender = validated_data["gender"] if "address" in validated_data.keys() else "U"
        instance.address = validated_data["address"] if "address" in validated_data.keys() else ""
        instance.note = validated_data["note"] if "note" in validated_data.keys() else ""
        instance.save()

        customer_groups = validated_data["customer_group"]
        instance.customer_group.clear()
        for cg in customer_groups:
            instance.customer_group.add(cg)
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

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', )

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
    customer_group = CustomerGroupSerializer(read_only=True, many=True)
    # gender = serializers.CharField(source='get_gender_display')
    # type = serializers.RelatedField(many=True)
    class Meta:
        model = Customer
        fields = ('customer_id', 'customer_group', 'fullname', 'gender', 'note', 'phone', 'address')

    # def get_gender(self, obj):
    #     return obj.get_gender_display()

class ResponseCustomerSerializer(ResponeSerializer):
    data = ReadCustomerSerializer()