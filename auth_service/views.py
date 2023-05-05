from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import authenticate

from .authentication import CustomAuthentication
from .models import Customer
from .serializer  import CustomerSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication, JWTStatelessUserAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.transaction import atomic
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }
@api_view(['POST'])
def login(request):
    serializer = CustomerSerializer(request.data)
    response = Response()
    user = authenticate(**serializer.data)
    if user:
        jwt = get_tokens_for_user(user)
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=jwt['access_token'],
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        response.set_cookie(
            key='refresh_token',
            value=jwt['refresh_token'],
            expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        # response.headers[settings.SIMPLE_JWT['AUTH_HEADER_NAME']] = settings.SIMPLE_JWT['AUTH_HEADER_TYPES'][0]+' '+data['access']
        response.data = jwt
        response.status_code = status.HTTP_200_OK
        return response
    else:
        return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def logout(request):
    response = Response(data = {'success': True},status = status.HTTP_200_OK)
    response.delete_cookie("access_token",)
    response.delete_cookie("refresh_token")

    return response




@api_view(['POST'])
def create_user(request):
    serializer = CustomerSerializer(data = request.data)
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


