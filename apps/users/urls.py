from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from users.views import UserModelViewSet

actions = {'get': 'get', 'post': 'create', 'patch': 'partial_update', 'put': 'update', 'delete': 'destroy'}
urlpatterns = [
    path('user', UserModelViewSet.as_view(actions), name='user'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]
