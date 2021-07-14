import os.path
from os import path

import pytz
from django.core.management.base import BaseCommand

from accounts.models import Log


class Command(BaseCommand):

    from_timezone = ''

    def validate_timezone(self, timezone_str):
        if timezone_str in pytz.all_timezones:
            return timezone_str
        else:
            raise ValueError('Invalid timezone string!')

    def add_arguments(self, parser):
        parser.add_argument('from-timezone', type=self.validate_timezone)

    __CONVERT_TO_UTC_FLAG = '.to_utc'

    def log_info(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def get_to_utc_flag(self):
        return path.exists(self.__CONVERT_TO_UTC_FLAG)

    def set_to_utc_flag(self, flag):

        if flag == self.get_to_utc_flag(
        ):    # do nothing if flag value is already set
            self.log_info(f'flag value is already {flag}')
            return

        if flag:    # create file if flag is True
            with open(self.__CONVERT_TO_UTC_FLAG, 'w') as file:
                pass
            self.log_info(f'flag value is now True')
        else:    # delete file if flag is False
            os.remove(self.__CONVERT_TO_UTC_FLAG)
            self.log_info(f'flag value is now False')

    def tz_to_utc(self, date_in_ptc):
        tz = pytz.timezone(self.from_timezone)
        date_in_utc = tz.normalize(tz.localize(date_in_ptc)).astimezone(
            pytz.utc)
        return date_in_utc.replace(tzinfo=None)

    def utc_to_tz(self, date_in_utc):
        tz = pytz.timezone(self.from_timezone)
        date_in_ptc = pytz.utc.localize(date_in_utc,
                                        is_dst=None).astimezone(tz)
        return date_in_ptc.replace(tzinfo=None)

    def convert_logs_tz_to_utc(self, n):
        self.log_info('in convert_logs_tz_to_utc')
        logs = Log.objects.filter(timezone=self.from_timezone)[:n]

        if logs:
            for log in logs:
                log.created_at = self.tz_to_utc(log.created_at)
                log.timezone = 'UTC'

            Log.objects.bulk_update(logs, ['created_at', 'timezone'])

        else:
            self.log_info(f'no {self.from_timezone} logs found')
            self.set_to_utc_flag(False)

    def convert_logs_utc_to_tz(self, n):
        self.log_info('in convert_logs_utc_to_tz')
        logs = Log.objects.utc()[:n]

        if logs:
            for log in logs:
                log.created_at = self.utc_to_tz(log.created_at)
                log.timezone = self.from_timezone
            Log.objects.bulk_update(logs, ['created_at', 'timezone'])

        else:
            self.log_info('no utc logs found')
            self.set_to_utc_flag(True)

    def handle(self, *args, **options):
        self.from_timezone = options['from-timezone']
        if self.get_to_utc_flag():
            self.convert_logs_tz_to_utc(10)
        else:
            self.convert_logs_utc_to_tz(10)
