from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializer  import CreateCustomerSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.transaction import atomic
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
class CreateUser(APIView):
    def post(self,request):
        serializer = CreateCustomerSerializer(data = request.data)
        if serializer.is_valid():
            with atomic():
                User = get_user_model()
                try:
                    user = User.objects.create(**serializer.data)
                except:

                    return Response('user already created', status=status.HTTP_400_BAD_REQUEST)
                user.set_password(serializer.data['password'])
                user.save()
                jwt_token = get_tokens_for_user(user)
                response = Response(jwt_token, status=status.HTTP_201_CREATED)
                response.set_cookie('access_token',jwt_token['access_token'])
                response.set_cookie('refresh_token',jwt_token['refresh_token'])
                return  response


        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
