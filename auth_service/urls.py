from django.contrib import admin
from django.urls import path, include
from .views import CreateUser, Login,Logout


urlpatterns = [
    path('signup/',CreateUser.as_view(),name = 'sign up'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

]