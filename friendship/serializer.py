from rest_framework import serializers

from auth_service.models import Customer


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class AcceptSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    accept = serializers.BooleanField()
class ResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    detail = serializers.CharField(max_length='255')


class RecursiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','username']

class CustomerSerializer(serializers.ModelSerializer):
    subscriptions = RecursiveSerializer(many=True, read_only=True)
    followers =  RecursiveSerializer(many=True, read_only=True)
    friends = RecursiveSerializer(many=True, read_only=True)
    class Meta:
        depth = 0
        model = Customer
        fields =['id','username', 'subscriptions', 'friends','followers']




