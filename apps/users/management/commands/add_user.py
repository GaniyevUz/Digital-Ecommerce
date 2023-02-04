from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('users_count', nargs='+', type=int)

    def handle(self, *args, **options):
        if c := options.get('poll_ids', 15):
            self.stdout.write(self.style.SUCCESS('Successfully closed poll !'))
