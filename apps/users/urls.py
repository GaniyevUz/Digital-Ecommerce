from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from users.views import UserUpdateDestroyAPIView

list_ = {'get': 'get', 'post': 'create'}
detail = {'patch': 'patch', 'put': 'put', 'delete': 'delete'}

urlpatterns = [
    path('user/', UserUpdateDestroyAPIView.as_view(list_), name='user-list'),
    path('user/<int:pk>/', UserUpdateDestroyAPIView.as_view(detail), name='user-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
