from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Create superuser with password: '1', email: 'admin@example.com'"

    def handle(self, *args, **options):
        user = User.objects.create_superuser('admin@example.com', '1')
        print(f'\033[43m<SuperUser {user}: email=admin@example.com>\033[92m  Created!\033[00m')
