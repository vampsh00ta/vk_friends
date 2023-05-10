from django.db.models import Q
from django.db.transaction import atomic
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.types import OpenApiTypes

from rest_framework.decorators import authentication_classes, permission_classes, api_view, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from auth_service.authentication import CustomAuthentication
from rest_framework.views import APIView
from .swagger_descriptions import send_request, accept_request, remove_friend, get_user, profile, get_status
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
        description= send_request,
        responses=ResponseSerializer,
    )
    def post(self,request):
        serializer = self.serializer_class(data = request.data)

        if serializer.is_valid():
            data = serializer.data
            friend_id = data['id']
            with atomic():
                user = request.user
                if friend_id == user.id:
                    return Response(data={"success": False,'detail':'cant added yourself'}, status=status.HTTP_400_BAD_REQUEST)
                friend = Customer.objects.filter(id=friend_id).first()
                if not friend:
                    return Response(data={"success": False,'detail':'theres no such user'}, status=status.HTTP_404_NOT_FOUND)
                request_in_friend = FriendshipRequest.objects.filter(from_person=user, to_person=friend).first()
                if request_in_friend:
                    return Response(data={"success": False,'detail':'already following'}, status=status.HTTP_200_OK)

                result = add_request_or_add_friend(user,friend)
            return Response(data = {"success":True,'detail':result},status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AcceptRequest(APIView):
    serializer_class = AcceptSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    @extend_schema(
        description=accept_request,
        responses=ResponseSerializer,
    )
    def post(self, request:Request)->Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.data
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
        return Response(data = serializer.errors,status = status.HTTP_400_BAD_REQUEST)


class RemoveFriend(APIView):
    serializer_class = IdSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    @extend_schema(
        description=remove_friend,
        responses=ResponseSerializer,
    )
    def post(self, request:Request)->Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            with atomic():
                user = request.user
                id = data["id"]
                if user.id == id:
                    return Response({"success": False, "detail":"cant remove yourself "})
                friend = Customer.objects.filter(id = id).first()
                if friend not in user.friends.all():
                    return Response(data = {"success":False,"detail":"not your friend"},status=status.HTTP_400_BAD_REQUEST)
                remove_from_friend_list(user,friend)
            return Response(data = {"success": True,'detail':'removed from friend list'},status =status.HTTP_200_OK )
        return Response(data = serializer.errors,status = status.HTTP_400_BAD_REQUEST)



class GetUser(APIView):
    @extend_schema(
        description=get_user,

        responses=CustomerSerializer,
    )
    def get(self,request:Request,id:int)->Response:
        user = Customer.objects.prefetch_related('friends').prefetch_related('subscriptions').filter(id=id).first()
        if not user:
            return Response(data={"success":False,"detail":'theres no such user'},status = status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(user)
        return Response(data=serializer.data)

class Profile(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]

    @extend_schema(
        description=profile,

        responses=CustomerSerializer,
    )
    def get(self,request:Request)->Response:
        user = request.user
        serializer = CustomerSerializer(user)
        return Response(data=serializer.data)


class GetStatus(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomAuthentication]
    @extend_schema(
    description=get_status,
        responses=ResponseSerializer,
    )
    def get(self, request, id):
        user = request.user
        requested_user = Customer.objects.filter(id = id).first()
        if not requested_user:
            return Response({"success":False,"detail":"theres no such user"},status = status.HTTP_404_NOT_FOUND)
        request_status  = FriendshipRequest.objects.filter(
            Q(from_person =user,to_person = requested_user )|Q(from_person =requested_user,to_person = user)
        ).first()
        if request_status:
            if request_status.from_person == user:
                return Response({"success":True,f"detail":f"you subscribed on {requested_user.username}"})
            return Response({"success": True, f"detail": f"{requested_user.username} subscribed on you"})

        if requested_user in user.friends.all():
            return Response({"success": True, f"detail": f"you are friends"},status = status.HTTP_200_OK)
        return Response({"success": True, f"detail": f"you dont have any relations"},status = status.HTTP_200_OK)
