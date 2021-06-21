from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views import View

from .forms import UserProfileForm
from .models import UserProfile


class SignUpView(View):
    template_name = 'registration/register.html'
    form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

        return render(request, self.template_name, {'form': form})


class UserProfileView(View):
    template_name = 'accounts/profile.html'
    form_class = UserProfileForm

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        form = self.form_class(instance=user_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        form = self.form_class(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, self.template_name, {'form': form})

