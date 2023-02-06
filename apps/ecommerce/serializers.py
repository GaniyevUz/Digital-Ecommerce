from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from ecommerce.models import Client


class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'email',
                  'phone', 'account_type',)


class CreateClientModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        validators.UniqueValidator(queryset=Client.objects.values_list('email', flat=True))])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = Client
        fields = ('password', 'confirm_password',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        attrs.pop('confirm_password')
        return attrs

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = Client.objects.create(**validated_data)
        # user.is_active = False
        # user.save()
        return user
