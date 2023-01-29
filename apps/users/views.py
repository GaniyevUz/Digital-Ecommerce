from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import RegisterModelSerializer, UserModelSerializer


class UserModelViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = RegisterModelSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return [User.objects.get(pk=self.request.user.pk)]
