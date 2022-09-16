from rest_framework import serializers

class ResponeSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    data = serializers.DictField()
    message = serializers.CharField(required = False)

class ResponeSuccessSerializer(ResponeSerializer):
    code = serializers.IntegerField(initial=1)
    data = serializers.DictField(initial=None)
    message = serializers.CharField(initial="success")