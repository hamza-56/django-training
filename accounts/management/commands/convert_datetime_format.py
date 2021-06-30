import os.path
from os import path

import pytz
from django.core.management.base import BaseCommand

from accounts.models import Log


class Command(BaseCommand):

    PST = 'Asia/Karachi'

    __CONVERT_PST_TO_UTC_FLAG = '.pst_to_utc'

    def log_info(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def get_pst_to_utc_flag(self):
        return path.exists(self.__CONVERT_PST_TO_UTC_FLAG)

    def set_pst_to_utc_flag(self, flag):

        if flag == self.get_pst_to_utc_flag(
        ):    # do nothing if flag value is already set
            self.log_info(f'flag value is already {flag}')
            return

        if flag:    # create file if flag is True
            with open(self.__CONVERT_PST_TO_UTC_FLAG, 'w') as file:
                pass
            self.log_info(f'flag value is now True')
        else:    # delete file if flag is False
            os.remove(self.__CONVERT_PST_TO_UTC_FLAG)
            self.log_info(f'flag value is now False')

    def pst_to_utc(self, date_in_ptc):
        tz = pytz.timezone(self.PST)
        date_in_utc = tz.normalize(tz.localize(date_in_ptc)).astimezone(
            pytz.utc)
        return date_in_utc.replace(tzinfo=None)

    def utc_to_pst(self, date_in_utc):
        tz = pytz.timezone(self.PST)
        date_in_ptc = pytz.utc.localize(date_in_utc,
                                        is_dst=None).astimezone(tz)
        return date_in_ptc.replace(tzinfo=None)

    def convert_logs_pst_to_utc(self, n):
        self.log_info('in convert_logs_pst_to_utc')
        logs = Log.objects.filter(timezone=self.PST)[:n]

        if logs:
            for log in logs:
                log.created_at = self.pst_to_utc(log.created_at)
                log.timezone = 'UTC'

            Log.objects.bulk_update(logs, ['created_at', 'timezone'])

        else:
            self.log_info('no pst logs found')
            self.set_pst_to_utc_flag(False)

    def convert_logs_utc_to_pst(self, n):
        self.log_info('in convert_logs_utc_to_pst')
        logs = Log.objects.filter(timezone='UTC')[:n]

        if logs:
            for log in logs:
                log.created_at = self.utc_to_pst(log.created_at)
                log.timezone = self.PST
            Log.objects.bulk_update(logs, ['created_at', 'timezone'])

        else:
            self.log_info('no utc logs found')
            self.set_pst_to_utc_flag(True)

    def handle(self, *args, **options):
        if self.get_pst_to_utc_flag():
            self.convert_logs_pst_to_utc(10)
        else:
            self.convert_logs_utc_to_pst(10)
