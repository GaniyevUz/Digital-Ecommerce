import re

import requests
from rest_framework import status

from shops.models import Shop, TelegramBot


class EmailValidator:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    def __call__(self, value) -> bool:
        return bool(re.fullmatch(self.regex, value))


class TelegramBotValidator:

    # def __init__(self, token, **kwargs) -> None:
    #     self.token = token
    #     self.kwargs = kwargs

    def __call__(self, token, **kwargs):
        if not kwargs.get('pk') or not Shop.objects.filter(pk=kwargs['pk']).exists():
            return {'status': 'Invalid shop'}
        get_me_url = f'https://api.telegram.org/bot{token}/getMe'
        response = requests.get(get_me_url).json()
        is_valid = response.get('ok')
        data = {}
        if is_valid:
            data['token'] = token
            data['username'] = response.get('result')['username']
            data['shop'] = Shop.objects.get(pk=kwargs['pk'])
            if TelegramBot.objects.filter(token=token).exists():
                return {
                    'data': {
                        'token': ['A bot with this token has already been registered in the system']
                    },
                    'status': status.HTTP_422_UNPROCESSABLE_ENTITY}
            return data
        return {'data': response, 'status': response.get('error_code')}
