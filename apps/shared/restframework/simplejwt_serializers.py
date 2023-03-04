from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import exceptions, serializers
from rest_framework_simplejwt import tokens, settings, serializers as jwt_serializers


class CustomTokenObtainSerializer(jwt_serializers.TokenObtainSerializer):  # noqa pylint: disable=abstract-method
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = jwt_serializers.PasswordField()
        self.fields['shop'] = serializers.HiddenField(required=False, default=None)

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
            'shop': attrs.get('shop'),
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not settings.api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):  # noqa pylint: disable=abstract-method
    token_class = tokens.RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if settings.api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
