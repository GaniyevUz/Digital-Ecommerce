from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from ecommerce.models import Client
from ecommerce.serializers import ClientModelSerializer, ClientCheckSerializer, LoginClientModelSerializer, \
    CreateClientModelSerializer
from shared.mixins import ShopRequiredMixin


class ClientUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, ShopRequiredMixin):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()

    def get_object(self):
        if self.request.user.is_anonymous or self.request.user.is_superuser:
            return None
        return self.request.user


class ClientModelViewSet(ModelViewSet, ShopRequiredMixin):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()
    permission_classes = AllowAny,
    email = openapi.Parameter('email', openapi.IN_QUERY, "check email address", True, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[email])
    def get(self, request, *args, **kwargs):
        serializer = ClientCheckSerializer(request.GET)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        post_data = request.POST if request.POST else request.data
        if post_data.get('email') and post_data.get('password'):
            user = Client.objects.get(email=post_data['email'])
            if user and check_password(post_data['password'], user.password):
                jwt = RefreshToken.for_user(user)
                data = {
                    'refresh': str(jwt),
                    'access': str(jwt.access_token),
                    'user': ClientModelSerializer(user).data
                }
                return Response(data)
        return Response({"password": ["Wrong username or password specified"]}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'post':
            return LoginClientModelSerializer
        return super().get_serializer_class()


class CreateClientAPIView(CreateAPIView, ShopRequiredMixin):
    serializer_class = CreateClientModelSerializer
    permission_classes = AllowAny,
