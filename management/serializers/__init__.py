from rest_framework import serializers

class ResponeSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    data = serializers.DictField()
    message = serializers.CharField(required = False)

# class ResponeSuccessSerializer(ResponeSerializer):
#     data = serializers.DictField()