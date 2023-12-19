from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user.models import User
from user.serializers import UserSerializer


class UserActivityView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        activity = {
            "last_request_time": request.last_request_time,
            "last_login_time": user.last_login,
        }
        return Response(activity)
