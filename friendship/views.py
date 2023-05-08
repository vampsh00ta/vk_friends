from django.db.transaction import atomic

from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import status
from auth_service.authentication import CustomAuthentication
from .serializer import CutomerSerializer, IdSerializer, AcceptSerializer
from .utils import add_request_or_add_friend, add_to_friendship
from auth_service.models import Customer

from auth_service.models import FriendshipRequest



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def send_request(request):
    serializer = IdSerializer(data = request.data)
    if serializer.is_valid():
        friend_id = serializer.validated_data['id']
        user = request.user
        if friend_id == user.id:
            return Response(data={"status": f'cant added yourself'}, status=status.HTTP_400_BAD_REQUEST)
        friend = Customer.objects.get(id=friend_id)
        with atomic():
            request_in_friend = FriendshipRequest.objects.filter(from_person=user, to_person=friend).first()
            if request_in_friend:
                return Response(data={"status": f'already following {friend.username}'}, status=status.HTTP_200_OK)

            result = add_request_or_add_friend(user,friend)
            return Response(data = {"status":result},status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_data(request,id):
    user = Customer.objects.get(id=id)
    serializer = CutomerSerializer(user)
    return Response(data=serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def accept_request_in_friends(request):
    serializer = AcceptSerializer(data=request.data)
    user = request.user
    if serializer.is_valid():
        data = serializer.validated_data
        user_request = Customer.objects.get(id = data['id'])
        request_in_friend = FriendshipRequest.objects.filter(from_person=user_request, to_person=user).first()
        if not request_in_friend:
            return  Response({"status":f"theres not such {user_request.username}`s request"}, status=status.HTTP_400_BAD_REQUEST)
        #if user wants to add other user in friendship
        if data['accept']:
            with atomic():
                add_to_friendship(user,user_request)
            return Response({"status":f"accepted  {user_request.username}`s request in friend list"}, status=status.HTTP_400_BAD_REQUEST)
        # if user wants to add other user in friendship
        request_in_friend.delete()
        return Response({"status": f"declined {user_request.username}`s request in friend list"}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def profile(request):
    user = request.user
    serializer = CutomerSerializer(user)
    return Response(data=serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([CustomAuthentication])
def delete_from_friendship(request):
    serializer = IdSerializer(data = request.data)
    if serializer.is_valid():
        user = request.user
        id = serializer.validated_data['id']
        # user.prefetch_related('friends')
        friend = Customer.objects.filter(id = id).first()
        if friend not in user.friends.all():
            return Response({"status":f"user {friend.username} is not your friend"})
        with atomic():
            request_in_friend = FriendshipRequest.objects.filter(from_person=user, to_person=friend).first()
            if request_in_friend:
                request_in_friend.delete()
            user.friends.remove(friend)
            friend.friends.remove(user)
        return Response({"status": f"deleted {friend.username} from friend list"})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)