from django import template

from accounts.models import Log, User

register = template.Library()


@register.simple_tag
def users_count():
    return User.objects.count()


@register.simple_tag
def pst_logs_count():
    return Log.objects.filter(timezone='Asia/Karachi').count()


@register.simple_tag
def utc_logs_count():
    return Log.objects.filter(timezone='UTC').count()
