from django.contrib import admin
from django.urls import path, include

from .views import send_request, get_data, accept_request_in_friends, delete_from_friendship, profile

urlpatterns = [
    path('sendRequest/',send_request),
    path('user/<int:id>',get_data),
    path('friendshipRequest/',accept_request_in_friends),
    path('deleteFriend/',delete_from_friendship),
    path('profile/',profile)

]