from django.urls import path

from ecommerce.views import ClientUpdateDestroyAPIView, CreateClientAPIView, ClientModelViewSet

urlpatterns = [
    path('sign-in', ClientModelViewSet.as_view({'get': 'get', 'post': 'post'})),
    path('sign-up', CreateClientAPIView.as_view()),
    path('profile/personal-info', ClientUpdateDestroyAPIView.as_view()),
]
