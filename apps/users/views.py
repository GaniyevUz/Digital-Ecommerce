from rest_framework.decorators import action
from rest_framework.decorators import action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSetMixin

from shared.tokens import one_time_token
from .models import User
from .serializers import UserModelSerializer, CreateUserModelSerializer


class UserModelViewSet(ModelViewSet):
    # permission_classes = (AllowAny,)
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserModelSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        self.permission_classes = (AllowAny,)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data)
    #
    # @action(methods=['GET'], detail=True, url_name='botir', url_path='botirjon')
    # def nimadir(self, pk):
    #     return Response({'status': True})
    #


class UserUpdateDestroyAPIView(ViewSetMixin, RetrieveUpdateDestroyAPIView, CreateAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    # http_method_names = 'PATCH', 'DELETE'
    def get(self, request, *args, **kwargs):
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserModelSerializer
        return super().get_serializer_class()
