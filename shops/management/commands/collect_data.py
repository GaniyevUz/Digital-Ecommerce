from django.core.management.base import BaseCommand

from commands import CollectDATA


class Command(BaseCommand):
    help = 'Create Default Objects'

    def handle(self, *args, **options):
        try:
            CollectDATA().collect_all()
            self.stdout.write(self.style.SUCCESS('Successfully collected data'))
        except Exception as e:
            raise e
