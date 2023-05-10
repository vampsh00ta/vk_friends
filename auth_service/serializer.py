from rest_framework import serializers
from rest_framework import serializers

from .models import Customer
class JwtResponse(serializers.Serializer):
    access_token = serializers.CharField(max_length=100)
    refresh_token = serializers.CharField(max_length=100)


class CustomerAuthSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


