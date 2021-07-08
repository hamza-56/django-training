from django.db.models import base
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import ListUsers, LogViewSet

router = routers.DefaultRouter()
router.register(r'logs', LogViewSet)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('token-auth/', obtain_auth_token, name='api_token_auth'),
    path('users/', ListUsers.as_view()),
    path('', include(router.urls)),
]
