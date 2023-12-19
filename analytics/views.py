from datetime import timedelta, datetime

from user.models import User
from user.serializers import UserSerializer
from network.models import Like

from rest_framework.views import APIView
from django.db.models import Count, F
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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


class AnalyticsView(APIView):
    def get(self, request, *args, **kwargs):
        date_from = request.query_params.get(
            "date_from",
            (datetime.now().date() + timedelta(days=-30)).isoformat(),
        )
        date_to = request.query_params.get(
            "date_to", datetime.now().date().isoformat()
        )

        try:
            date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = datetime.strptime(date_to, "%Y-%m-%d").date()

        except ValueError:
            return Response(
                {"error": "Invalid date format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except TypeError:
            return Response(
                {"error": "Empty date"}, status=status.HTTP_400_BAD_REQUEST
            )

        likes_count = (
            (Like.objects.filter(created_at__date__range=[date_from, date_to]))
            .values(date=F("created_at__date"))
            .order_by("-date")
            .annotate(likes_count=Count("id"))
        )

        return Response(likes_count)
