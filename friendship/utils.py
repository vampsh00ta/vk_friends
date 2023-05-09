from django.contrib.auth.models import User

from auth_service.models import Customer,FriendshipRequest
from django.db.models import Q

from .models import OldRequest
# def if_subscriber(user:Customer,friend:Customer):
#     request_in_friend = FriendshipRequest.objects.filter(from_person=friend, to_person=user).first()
#     return request_in_friend

def add_to_friendship(request_in_friend:FriendshipRequest,user:Customer,friend:Customer):
    request_in_friend.delete()
    old_req = OldRequest(from_person = friend, to_person = user)
    old_req.save()
    user.friends.add(friend)
    friend.friends.add(user)
def remove_from_friend_list(user:Customer,friend):
    old_req = OldRequest.objects.filter(
        Q(from_person=friend, to_person=user) or Q(from_person=user, to_person=friend  )
    ).first()
    if old_req.from_person == friend:
        req = FriendshipRequest(from_person=old_req.from_person, to_person=old_req.to_person)
        req.save()
    old_req.delete()
    user.friends.remove(friend)
    friend.friends.remove(user)
def add_request_or_add_friend(user:Customer,friend:Customer):
    request_in_friend = FriendshipRequest.objects.filter(from_person=friend, to_person=user).first()

    if request_in_friend:
        add_to_friendship(request_in_friend,user,friend)
        return f'added {friend.username} to friendship '
    FriendshipRequest.objects.create(from_person=user, to_person=friend)

    return f'request to {friend.username} user friendship'

