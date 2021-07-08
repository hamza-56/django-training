from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from accounts.models import User


class Command(BaseCommand):
    help = 'Creates specified number of users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        for i in range(options['count']):
            username = get_random_string(length=5)
            password = get_random_string(length=8)
            User.objects.create_user(username=username, password=password)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {i + 1} user with username {username}, password: {password}'
                ))
