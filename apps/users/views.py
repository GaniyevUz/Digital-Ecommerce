from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import RegisterModelSerializer, UserModelSerializer, CreateUserModelSerializer


class UserModelViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterModelSerializer
        return super().get_serializer_class()

    # TODO: qarab chiqish kk
    @action(methods=['GET'], detail=True, url_name='botir', url_path='botirjon')
    def nimadir(self, pk):
        return Response({'status': True})


class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = RegisterModelSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return [User.objects.get(pk=self.request.user.pk)]
