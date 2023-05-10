
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import authenticate

from .authentication import get_tokens_for_user, set_jwt_cookie

from .serializer import CustomerAuthSerializer, JwtResponse
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from .swagger_descriptions import login,logout,register
from friendship.serializer import ResponseSerializer

class Logout(APIView):

    @extend_schema(
        description=logout,
        responses=ResponseSerializer,
    )
    def post(self,request):
        response = Response(data={'success': True,'detail':"logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("access_token", )
        response.delete_cookie("refresh_token")
        return response
class Login(APIView):
    serializer_class = CustomerAuthSerializer

    @extend_schema(
        description=login,

        request=CustomerAuthSerializer,
        responses= JwtResponse,
    )
    def post(self,request):

        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            response = Response()

            data = serializer.data
            user = authenticate(**data)
            if user:
                jwt = get_tokens_for_user(user)
                response = set_jwt_cookie(response, jwt)
                response.data = jwt
                response.status_code = status.HTTP_200_OK
                return response
            else:
                return Response({"success": False,"detail":"invalid username or password!"}, status=status.HTTP_404_NOT_FOUND)
        return Response(data = serializer.errors,status = status.HTTP_400_BAD_REQUEST)

class CreateUser(APIView):
    serializer_class = CustomerAuthSerializer

    @extend_schema(
        description=register,

        request=CustomerAuthSerializer,
        responses=JwtResponse,
    )
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with atomic():
                data = serializer.data
                User = get_user_model()
                try:
                    user = User.objects.create(**data)
                except:

                    return Response(data = {'success':False,'detail':'user already created'}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(data['password'])
                user.save()
                jwt = get_tokens_for_user(user)
                response = Response()
                response = set_jwt_cookie(response, jwt)
                response.status_code = status.HTTP_201_CREATED
                return  response
        return Response(data = serializer.errors,status = status.HTTP_400_BAD_REQUEST)




