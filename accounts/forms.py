from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', )


class ProfileUpdateForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm):
        model = User
        fields = ('first_name', 'last_name', 'birth_date', 'bio')
        fields_order = ('first_name', 'last_name', 'birth_date', 'bio')
        widgets = {'birth_date': forms.DateInput(attrs={'type': 'date'})}
