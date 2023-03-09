from django.core.management.base import BaseCommand
from django.db import connection

from shared.utils import get_summ_all, get_stat_sales, get_avarage_price


class Command(BaseCommand):
    help = 'Creating PostgreSQL function'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            functions = get_summ_all + get_avarage_price + get_stat_sales
            try:
                cursor.execute(functions)
            except Exception as ex:
                print(ex)
