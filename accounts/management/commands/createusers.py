from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from accounts.models import User


class Command(BaseCommand):
    help = 'Creates specified number of users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        n = options['count']
        passwords = [get_random_string(length=8) for _ in range(n)]
        users = [
            User(username=get_random_string(length=5),
                 password=make_password(passwords[i])) for i in range(n)
        ]
        User.objects.bulk_create(users)

        for user, password in zip(users, passwords):
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created user with username {user.username}, password: {password}'
                ))
