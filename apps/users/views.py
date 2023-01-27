from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import RegisterModelSerializer, UserModelSerializer


class UserModelViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        self.serializer_class = RegisterModelSerializer
        return super().create(request, *args, **kwargs)
