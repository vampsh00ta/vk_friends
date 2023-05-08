from rest_framework import serializers

from auth_service.models import Customer


class IdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class AcceptSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    accept = serializers.BooleanField()


class RecursiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','username']


class CutomerSerializer(serializers.ModelSerializer):
    subscribed_on = RecursiveSerializer(many=True, read_only=True)
    followed_by =  RecursiveSerializer(many=True, read_only=True)
    friends = RecursiveSerializer(many=True, read_only=True)
    class Meta:
        depth = 0
        model = Customer
        fields =['id','username', 'subscribed_on', 'friends','followed_by']


