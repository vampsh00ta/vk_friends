from django.contrib import admin
from django.urls import path, include

from .views import AcceptRequest, SendRequest, GetUser, Profile, RemoveFriend

urlpatterns = [
    path('sendRequest/',SendRequest.as_view()),
    path('user/<int:id>',GetUser.as_view()),
    path('friendshipRequest/',AcceptRequest.as_view()),
    path('deleteFriend/',RemoveFriend.as_view()),
    path('profile/',Profile.as_view())

]