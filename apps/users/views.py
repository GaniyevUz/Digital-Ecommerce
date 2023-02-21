from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSetMixin

from .models import User
from .serializers import UserModelSerializer, CreateUserModelSerializer


class UserUpdateDestroyAPIView(ViewSetMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    # http_method_names = 'PATCH', 'DELETE'
    def get(self, request, *args, **kwargs):
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data)


class UserCreateAPIView(CreateAPIView):
    serializer_class = CreateUserModelSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny,
