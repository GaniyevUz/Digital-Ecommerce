from shops.models import Currency


def collect_shops_currencies() -> None:
    currencies = ("UZS", "RUB", "KZT", "UAH", "KGS", "TJS", "AZN", "AFN", "USD", "KRW")
    for currency in currencies:
        obj = Currency.objects.create(name=currency)
        print(f"<Currency object: id={obj.pk}, name={obj.name}>")
