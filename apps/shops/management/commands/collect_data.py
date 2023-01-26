from django.core.management.base import BaseCommand

from shops.models import ShopCategory, ShopCurrency


class CollectDATA:
    @staticmethod
    def collect_shops_categories() -> None:
        categories = (
            "Clothing", "Electronics", "Books, Movies,  Music and Games", "Cosmetics", "Bags and Accessories", "food",
            "Appliances", "Furniture and Household Goods", "Sport and Leisure", "Toys and Baby Products", "Stationery",
            "Garden & Pets", "Other"
        )
        for category in categories:
            obj = ShopCategory.objects.create(name=category)
            print(f"<ShopCategory object: id={obj.pk}, name={obj.name}>")

    @staticmethod
    def collect_shops_currencies() -> None:
        currencies = ("UZS", "RUB", "KZT", "UAH", "KGS", "TJS", "AZN", "AFN", "USD", "KRW")
        for currency in currencies:
            obj = ShopCurrency.objects.create(name=currency)
            print(f"<ShopCurrency object: id={obj.pk}, name={obj.name}>")

    def collect_all(self) -> None:
        self.collect_shops_categories()
        self.collect_shops_currencies()


class Command(BaseCommand):
    help = 'Create Default Objects'

    def handle(self, *args, **options):
        try:
            CollectDATA().collect_all()
            self.stdout.write(self.style.SUCCESS('Successfully collected data'))
        except Exception as e:
            raise e
