from django.db.transaction import atomic
from drf_spectacular.types import OpenApiTypes

from rest_framework.decorators import authentication_classes, permission_classes, api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from rest_framework.response import Response
from rest_framework import status
from auth_service.authentication import CustomAuthentication
from rest_framework.views import APIView

from .serializer import CustomerSerializer, IdSerializer, AcceptSerializer, ResponseSerializer
from .utils import add_request_or_add_friend, add_to_friendship, remove_from_friend_list
from auth_service.models import Customer
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_field

from auth_service.models import FriendshipRequest






class SendRequest(APIView):
    serializer_class = IdSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    @extend_schema(

        responses=ResponseSerializer,
    )
    def post(self,request):
        friend_id = request.data
        with atomic():
            user = request.user
            if friend_id == user.id:
                return Response(data={"success": False,'detail':'cant added yourself'}, status=status.HTTP_400_BAD_REQUEST)
            friend = Customer.objects.get(id=friend_id)
            request_in_friend = FriendshipRequest.objects.filter(from_person=user, to_person=friend).first()
            if request_in_friend:
                return Response(data={"success": False,'detail':'already following'}, status=status.HTTP_200_OK)

            result = add_request_or_add_friend(user,friend)
        return Response(data = {"success":True,'detail':result},status=status.HTTP_200_OK)






class AcceptRequest(APIView):
    serializer_class = AcceptSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    @extend_schema(

        responses=ResponseSerializer,
    )
    def post(self, request:Request)->Response:
        data = request.data
        with atomic():
            user = request.user
            user_request = Customer.objects.filter(id=data['id']).first()
            # if not user_request:
            #     return Response({"success": False, "detail": "theres not such user"},
            #                     status=status.HTTP_400_BAD_REQUEST)

            request_in_friend = FriendshipRequest.objects.filter(from_person=user_request, to_person=user).first()
            if not request_in_friend :
                return Response({"success": False, "detail": "theres not such request or user"},
                                status=status.HTTP_400_BAD_REQUEST)
            # if user wants to add other user in friendship
            if data['accept']:
                add_to_friendship(request_in_friend, user, user_request)
                return Response({"success": True, "detail": "added to friend list"}, status=status.HTTP_200_OK)
            # if user wants to add other user in friendship
            request_in_friend.delete()
        return Response({"success": True, "detail": "declined  request in friend list"}, status=status.HTTP_200_OK)


class RemoveFriend(APIView):
    serializer_class = IdSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    @extend_schema(

        responses=ResponseSerializer,
    )
    def post(self, request:Request)->Response:
        with atomic():
            user = request.user
            id = request.data
            friend = Customer.objects.filter(id = id).first()
            if friend not in user.friends.all():
                return Response(data = {"success":False,"detail":"not your friend"},status=status.HTTP_400_BAD_REQUEST)
            remove_from_friend_list(user,friend)
        return Response(data = {"success": True,'detail':'removed from friend list'},status =status.HTTP_200_OK )

class GetUser(APIView):
    @extend_schema(

        responses=CustomerSerializer,
    )
    def get(self,request:Request,id:int)->Response:
        user = Customer.objects.prefetch_related('friends').prefetch_related('subscribed_on').filter(id=id).first()
        serializer = CustomerSerializer(user)
        return Response(data=serializer.data)

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    @extend_schema(

        responses=CustomerSerializer,
    )
    def get(self,request:Request)->Response:
        user = request.user
        serializer = CustomerSerializer(user)
        return Response(data=serializer.data)


