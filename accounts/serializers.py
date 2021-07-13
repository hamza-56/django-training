import pytz
from rest_framework import serializers

from .models import Log, User


class LogSerializer(serializers.HyperlinkedModelSerializer):
    def validate_timezone(self, timezone_str):
        if timezone_str not in pytz.all_timezones:
            raise serializers.ValidationError(
                f'Invalid timezone string {timezone_str}')
        return timezone_str

    class Meta:
        model = Log
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
        )


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'birth_date',
            'bio',
        )
