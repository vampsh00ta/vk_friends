from django.contrib import admin
from django.urls import path, include
from .views import create_user, login,logout






urlpatterns = [
    path('signup/',create_user),
    path('login/', login, name='token_obtain_pair'),
    path('logout/', logout, name='token_obtain_pair'),

    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]