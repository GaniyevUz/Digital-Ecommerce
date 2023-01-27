from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from rest_framework.routers import DefaultRouter
from users.views import UserModelViewSet

router = DefaultRouter()

router.register('users', UserModelViewSet, 'user')
urlpatterns = [
    path('', include(router.urls)),
    # path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
