from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import User
from .serializers import RegisterModelSerializer, UserModelSerializer


class UserModelViewSet(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


class UserProfileCreateAPIView(ListCreateAPIView):
    serializer_class = RegisterModelSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        serializer = UserModelSerializer(request.user)
        return Response(serializer.data)


