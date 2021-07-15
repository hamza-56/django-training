from django.db.models import base
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from .views import (ListUsers, LogViewSet, RegisterView, TodoListViewSet,
                    UserProfileRetrieveUpdateAPIView)

router = routers.DefaultRouter()
router.register(r'logs', LogViewSet)
router.register(r'todos', TodoListViewSet, basename='todos')

urlpatterns = [
    # path('auth/', include('rest_framework.urls')),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', obtain_auth_token, name='api_token_auth'),
    path('users/', ListUsers.as_view()),
    path('profile/<int:pk>/', UserProfileRetrieveUpdateAPIView.as_view()),
    path('', include(router.urls)),
]
