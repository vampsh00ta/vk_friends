from django.db.transaction import atomic

from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from auth_service.authentication import CustomAuthentication
from .serializer import CutomerSerializer, IdSerializer, AcceptSerializer
from .utils import add_request_or_add_friend, add_to_friendship, remove_from_friend_list
from auth_service.models import Customer

from auth_service.models import FriendshipRequest



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def send_request(request):
    serializer = IdSerializer(data = request.data)
    if serializer.is_valid():
        friend_id = serializer.validated_data['id']
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

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def accept_request_in_friends(request):
    serializer = AcceptSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        with atomic():
            user = request.user
            user_request = Customer.objects.get(id = data['id'])
            request_in_friend = FriendshipRequest.objects.filter(from_person=user_request, to_person=user).first()
            if not request_in_friend:
                return  Response({"success":False,"detail":"theres not such request"}, status=status.HTTP_400_BAD_REQUEST)
            #if user wants to add other user in friendship
            if data['accept']:
                add_to_friendship(request_in_friend,user,user_request)
                return Response({"success":True,"detail":"added to friend list"}, status=status.HTTP_200_OK)
            # if user wants to add other user in friendship
            request_in_friend.delete()
        return Response({"success":True,"detail":"declined  request in friend list" }, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def delete_from_friendship(request):
    serializer = IdSerializer(data = request.data)
    if serializer.is_valid():
        with atomic():
            user = request.user
            id = serializer.validated_data['id']
            friend = Customer.objects.filter(id = id).first()
            if friend not in user.friends.all():
                return Response(data = {"success":False,"detail":"not your friend"},status=status.HTTP_400_BAD_REQUEST)
            remove_from_friend_list(user,friend)
        return Response(data = {"success": True,'detail':'removed from friend list'},status =status.HTTP_200_OK )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_data(request,id):
    user = Customer.objects.prefetch_related('friends').prefetch_related('subscribed_on').filter(id=id).first()
    serializer = CutomerSerializer(user)
    return Response(data=serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def profile(request):
    user = request.user
    serializer = CutomerSerializer(user)
    return Response(data=serializer.data)
