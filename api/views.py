from rest_framework import authentication, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Log, User
from accounts.serializers import LogSerializer


class LogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
