from django.core.cache import cache
from rest_framework import mixins, permissions, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Log, User
from accounts.serializers import (LogSerializer, UserCreateSerializer,
                                  UserProfileSerializer)
from todolist.models import TodoListItem
from todolist.serialzers import TodoListItemSerializer

from .permissions import UserIsOwnerOrReadOnly


class LogViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Log.objects.all()
    serializer_class = LogSerializer

    LIST_CACHE_KEY = 'log_list'
    DETAIL_CACHE_KEY_PREFIX = 'log_details_'

    def _invalidate_list_cache(self):
        cache_key = self.LIST_CACHE_KEY
        cache.delete(cache_key)

    def list(self, request):
        cache_key = self.LIST_CACHE_KEY

        data = cache.get(cache_key)
        if data:
            return Response(data)

        response = super().list(request)
        cache.set(cache_key, response.data)
        return response

    def retrieve(self, request, pk=None):
        cache_key = f'{self.DETAIL_CACHE_KEY_PREFIX}{pk}'

        data = cache.get(cache_key)
        if data:
            return Response(data)

        response = super().retrieve(request, pk=pk)
        cache.set(cache_key, response.data)
        return response

    def create(self, request):
        response = super().create(request)
        self._invalidate_list_cache()
        return response

    def update(self, request, pk=None):
        cache_key = f'{self.DETAIL_CACHE_KEY_PREFIX}{pk}'

        response = super().update(request, pk=pk)
        cache.set(cache_key, response.data)
        self._invalidate_list_cache()
        return response

    def destroy(self, request, pk=None):
        cache_key = f'{self.DETAIL_CACHE_KEY_PREFIX}{pk}'

        response = super().destroy(request, pk=pk)
        cache.set(cache_key, response.data)
        self._invalidate_list_cache()
        return response


class ListUsers(APIView):
    '''
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    '''
    permission_classes = (permissions.IsAdminUser, )

    def get(self, request, format=None):
        '''
        Return a list of all users.
        '''
        users = [
            user._asdict() for user in User.objects.values_list(
                'username', 'email', 'full_name', named=True)
        ]
        return Response(users)


class TodoListViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoListItemSerializer

    def get_queryset(self):
        user = self.request.user
        return TodoListItem.objects.filter(owner=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=user)


class RegisterView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer


class UserProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        UserIsOwnerOrReadOnly,
    )
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
