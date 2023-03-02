from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, validators
from rest_framework.fields import BooleanField
from rest_framework_simplejwt.tokens import RefreshToken

from shared.utils import EmailValidator, get_subdomain
from users.models import User


class ClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email',
                  'phone', 'account_type')


class ClientCheckSerializer(serializers.Serializer):  # noqa - ABC
    exists = BooleanField(help_text='Checks if the client is registered with this email address', read_only=True)

    def to_representation(self, instance):
        # TODO to optimize
        message = {'email': []}
        if email := instance.get('email'):
            email_validator = EmailValidator()
            if email_validator(email):
                exists = User.objects.filter(email=email).exists()
                return {'exists': exists}
            message['email'] = ['Enter a valid email address.']
            return message
        message['email'] = ['This field is required.']
        return message


class CreateClientModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
        validators.UniqueValidator(queryset=User.objects.values_list('email', flat=True))])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('password', 'confirm_password',
                  'email', 'first_name', 'last_name', 'phone', 'account_type')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        attrs.pop('confirm_password')
        return attrs

    def create(self, validated_data, **kwargs):
        validated_data['password'] = make_password(validated_data['password'])
        domain = get_subdomain(self.context['request']).shop
        user = User.objects.create(**validated_data, shop=domain)
        # user.is_active = False
        # user.save()
        return user

    def to_representation(self, user):
        jwt = RefreshToken.for_user(user)
        data = {
            'refresh': str(jwt),
            'access': str(jwt.access_token),
            'user': ClientModelSerializer(user).data
        }
        return data


class LoginClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'email')
