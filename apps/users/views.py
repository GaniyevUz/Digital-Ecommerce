from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.permisions import UserPermission
from .models import User
from .serializers import UserModelSerializer, CreateUserModelSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    permission_classes = (UserPermission,)

    def get_object(self):
        return self.request.user

    # http_method_names = 'PATCH', 'DELETE'
    def get(self, request, *args, **kwargs):
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.serializer_class = CreateUserModelSerializer
        return super().create(request, *args, **kwargs)
