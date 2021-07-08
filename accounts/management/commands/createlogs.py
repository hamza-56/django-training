from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from accounts.models import Log


class Command(BaseCommand):
    help = 'Creates specified number of logs'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        for i in range(options['count']):
            msg = get_random_string(length=20)
            PST = 'Asia/Karachi'
            created_at = datetime.now()
            Log.objects.create(msg=msg, timezone=PST, created_at=created_at)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {i + 1} log with msg {msg}, timezone: {PST}, created_at: {created_at}'
                ))
