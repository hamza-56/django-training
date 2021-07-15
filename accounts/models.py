from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_timezone


class User(AbstractUser):
    full_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)


class LogManager(models.Manager):
    def utc(self):
        return self.filter(timezone='UTC')

    def pst(self):
        return self.filter(timezone='Asia/Karachi')


class Log(models.Model):
    msg = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50, validators=[validate_timezone])
    created_at = models.DateTimeField()
    objects = LogManager()

    def __str__(self):
        return f'{self.msg} - {self.created_at} {self.timezone}'
