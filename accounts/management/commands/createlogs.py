import random
import string
from datetime import datetime

import pytz
from django.core.management.base import BaseCommand
from pytz import all_timezones_set, timezone

from accounts.models import Log


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(length))
    return result


class Command(BaseCommand):
    help = 'Creates specified number of logs'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int)

    def handle(self, *args, **options):
        for i in range(options['count']):
            msg = get_random_string(20)
            PST = 'Asia/Karachi'
            created_at = datetime.now(timezone(PST))
            Log.objects.create(msg=msg, timezone=PST, created_at=created_at)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created {i + 1} log with msg {msg}, timezone: {PST}, created_at: {created_at}'
                ))
