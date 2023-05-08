from django.contrib.auth.models import User

from auth_service.models import Customer,FriendshipRequest


def check_friendship(user:Customer,friend:Customer):
    request_in_friend = FriendshipRequest.objects.filter(from_person=friend,to_person=user).first()
    return request_in_friend
def add_to_friendship(user:Customer,friend):
    user.friends.add(friend)
    friend.friends.add(user)

def add_request_or_add_friend(user:Customer,friend:Customer):
    request_in_friend = FriendshipRequest.objects.filter(from_person=friend, to_person=user).first()

    if request_in_friend:
        add_to_friendship(user,friend)
        request_in_friend.delete()

        return f'added {friend.username} to friendship '
    FriendshipRequest.objects.create(from_person=user, to_person=friend)

    return f'request to {friend.username} user friendship'

