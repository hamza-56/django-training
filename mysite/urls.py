from django.contrib import admin
from django.urls import include, path

from .views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('', HomeView.as_view(), name='home')
]
