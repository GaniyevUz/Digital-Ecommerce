from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from shared.utils import email_validator
from users.models import User


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email',
            'invitation_token', 'default_shop', 'invitation',
            'date_joined', 'last_login'
        )


class CreateUserModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[email_validator])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
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
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user
