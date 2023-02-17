from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from users.views import UserUpdateDestroyAPIView

actions = {'get': 'get', 'patch': 'patch', 'put': 'put', 'delete': 'delete'}
urlpatterns = [
    path('user/', UserUpdateDestroyAPIView.as_view(actions), name='user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
