from re import fullmatch

from httpx import get
from rest_framework import status
from rest_framework.request import Request

from shops.models import Shop, TelegramBot, Domain


# ema
def email_validator(value) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return bool(fullmatch(regex, value))


class TelegramBotValidator:

    # def __init__(self, token, **kwargs) -> None:
    #     self.token = token
    #     self.kwargs = kwargs

    def __call__(self, token, **kwargs):
        if not kwargs.get('shop') or not Shop.objects.filter(pk=kwargs['shop']).exists():
            return {'status': 'Invalid shop'}
        get_me_url = f'https://api.telegram.org/bot{token}/getMe'
        response = get(get_me_url).json()
        data = {}
        if response.get('ok'):
            data['token'] = token
            data['username'] = response.get('result')['username']
            data['shop'] = Shop.objects.get(pk=kwargs['shop'])
            if TelegramBot.objects.filter(token=token).exists():
                return {
                    'data': {
                        'token': ['A bot with this token has already been registered in the system']
                    },
                    'status': status.HTTP_422_UNPROCESSABLE_ENTITY}
            return data
        return {'data': response, 'status': response.get('error_code')}


def get_subdomain(request: Request) -> Domain | bool:
    domains = request.get_host().split('.')
    if len(domains) >= 2:  # subdomain.example.com
        try:
            shop_domain = Domain.objects.get(name=domains[0])
            return shop_domain
        except (Domain.DoesNotExist, Domain.MultipleObjectsReturned):
            pass
    return False
