from django.contrib.auth.models import AbstractUser
from django.db import models
from pytz import timezone


class User(AbstractUser):
    full_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def save(self, *args, **kwargs):
        self.full_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)


class Log(models.Model):
    msg = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)
    created_at = models.DateTimeField()
