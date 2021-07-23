from datetime import datetime

from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

from accounts.models import Log


class Command(BaseCommand):
    help = 'Creates specified number of logs'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        n = options['count']
        PST = 'Asia/Karachi'
        logs = [
            Log(msg=get_random_string(length=20),
                timezone=PST,
                created_at=datetime.now()) for _ in range(n)
        ]
        Log.objects.bulk_create(logs)

        for log in logs:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created log with msg {log.msg}, timezone: {log.timezone}, created_at: {log.created_at}'
                ))
