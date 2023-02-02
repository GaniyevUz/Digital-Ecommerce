import uuid
from django.contrib.auth.tokens import default_token_generator
import six
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators

from users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# TODO jahongirga
class CreateUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class RegisterModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        validators.UniqueValidator(queryset=User.objects.values_list('email', flat=True))])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password',
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
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
