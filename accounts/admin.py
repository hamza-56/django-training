from django.contrib import admin

from .models import Log, User

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ('username', 'first_name', 'last_name', 'email', 'password')
    list_display = ('username', 'email', 'full_name')


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('msg', 'timezone')
    list_filter = ('timezone', )
