from django.contrib import admin
from django.urls import path, include

from .views import AcceptRequest, SendRequest, GetUser, Profile, RemoveFriend, GetStatus

urlpatterns = [
    path('sendRequest/',SendRequest.as_view()),
    path('user/<int:id>',GetUser.as_view()),
    path('friendlistRequest/',AcceptRequest.as_view()),
    path('deleteFriend/',RemoveFriend.as_view()),
    path('profile/',Profile.as_view()),
    path('relationStatus/<int:id>',GetStatus.as_view())

]