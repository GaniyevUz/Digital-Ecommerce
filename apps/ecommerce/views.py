from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSetMixin

from ecommerce.models import Client
from ecommerce.serializers import ClientModelSerializer, CreateClientModelSerializer


class ClientUpdateDestroyAPIView(ViewSetMixin, RetrieveUpdateDestroyAPIView, CreateAPIView):
    serializer_class = ClientModelSerializer
    queryset = Client.objects.all()

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        serializer = ClientModelSerializer(request.user)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateClientModelSerializer
        return super().get_serializer_class()
