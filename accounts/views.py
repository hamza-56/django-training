from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import CreateView

from .forms import ProfileUpdateForm, RegisterForm


class SignUpView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = '/accounts/login'


class UserProfileView(View):
    template_name = 'accounts/profile.html'
    form_class = ProfileUpdateForm

    def get(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user = request.user
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')

        return render(request, self.template_name, {'form': form})
