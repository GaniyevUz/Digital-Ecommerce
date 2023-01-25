from .shops_category import collect_shops_categories
from .shops_currency import collect_shops_currencies


class CollectDATA:
    """
    Collect data command as

    ./manage.py collect_data
    """

    def example_method(self) -> None:
        """you must write like"""
        pass

    @staticmethod
    def collect_shops_categories() -> None:
        collect_shops_categories()

    @staticmethod
    def collect_shops_currencies() -> None:
        collect_shops_currencies()

    def collect_all(self) -> None:
        """
        collect all method
        uou must add your own method here
        eg: self.example_method()
        """
        self.collect_shops_categories()
        self.collect_shops_currencies()
