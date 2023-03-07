from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.restframework import UserPermission
from .models import User
from .serializers import UserModelSerializer, CreateUserModelSerializer


class UserAPIViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = (UserPermission,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserModelSerializer
        return super().get_serializer_class()

    def get(self, request, *args, **kwargs):
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data)
