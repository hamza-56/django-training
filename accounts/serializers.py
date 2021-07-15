from rest_framework import serializers

from .models import Log, User


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        '''
        override create method to save hashed password
        '''
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
