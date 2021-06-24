from django import template

from accounts.models import User

register = template.Library()


@register.simple_tag
def users_count():
    return User.objects.count()
