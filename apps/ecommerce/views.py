from django.contrib.auth.hashers import check_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from shared.django import APIViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from ecommerce.serializers import ClientModelSerializer, ClientCheckSerializer, LoginClientModelSerializer, \
    CreateClientModelSerializer
from shared.django import BaseShopMixin
from users.models import User


class ClientUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView, BaseShopMixin):
    serializer_class = ClientModelSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class ClientAPIViewSet(APIViewSet, BaseShopMixin):
    serializer_class = ClientCheckSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny,
    email = openapi.Parameter('email', openapi.IN_QUERY, "check email address", True, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[email])
    def get(self, request, *args, **kwargs):
        serializer = ClientCheckSerializer(request.GET)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        post_data = request.POST if request.POST else request.data
        if post_data.get('email') and post_data.get('password'):
            user = User.objects.get(email=post_data['email'])
            if user and check_password(post_data['password'], user.password):
                jwt = RefreshToken.for_user(user)
                data = {
                    'refresh': str(jwt),
                    'access': str(jwt.access_token),
                    'user': ClientModelSerializer(user).data
                }
                return Response(data)
        return Response({"password": ["Wrong email or password specified"]}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'post':
            return LoginClientModelSerializer
        # if self.action == 'get':
        #     return ClientCheckSerializer
        return super().get_serializer_class()


class CreateClientAPIView(CreateAPIView, BaseShopMixin):
    serializer_class = CreateClientModelSerializer
    permission_classes = AllowAny,

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
