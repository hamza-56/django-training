import pytz
from django.core.exceptions import ValidationError


def validate_timezone(timezone_str):
    if timezone_str not in pytz.all_timezones:
        raise ValidationError(f'Invalid timezone string {timezone_str}')
    return timezone_str
