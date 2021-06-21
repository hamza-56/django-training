from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import include, path

from .views import SignUpView, UserProfileView

urlpatterns = [
    path('profile/',
         login_required(UserProfileView.as_view()),
         name='get_or_update_profile'),
    path('register/', SignUpView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls'))
]
