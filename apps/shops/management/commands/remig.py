import os

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Remove all tables from the database'

    def handle(self, *args, **options):
        cursor = connection.cursor()
        os.system('make unmig')
        sql = "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
        cursor.execute(sql)
        os.system('make mig')
