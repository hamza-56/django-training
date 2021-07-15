from rest_framework import authentication, mixins, permissions, viewsets
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
    authentication_classes = (authentication.TokenAuthentication, )
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class ListUsers(APIView):
    '''
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    '''
    permission_classes = (permissions.IsAdminUser, )
    authentication_classes = (authentication.TokenAuthentication, )

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
    authentication_classes = (authentication.TokenAuthentication, )
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
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
