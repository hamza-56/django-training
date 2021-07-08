import pytz
from rest_framework import serializers

from accounts.models import Log


class LogSerializer(serializers.HyperlinkedModelSerializer):
    def validate_timezone(self, timezone_str):
        if timezone_str not in pytz.all_timezones:
            raise serializers.ValidationError(
                f'Invalid timezone string {timezone_str}')
        return timezone_str

    class Meta:
        model = Log
        fields = '__all__'
