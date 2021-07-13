import pytz
from rest_framework import serializers

from .models import TodoListItem


class TodoListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoListItem
        exclude = ('owner', )
