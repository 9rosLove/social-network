from datetime import timedelta, datetime

from analytics.pagination import AnalyticsPagination
from analytics.serializers import LikeAnalyticsSerializer
from user.models import User
from user.serializers import UserSerializer
from network.models import Like

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


class LikeAnalyticsView(generics.ListAPIView):
    pagination_class = AnalyticsPagination
    serializer_class = LikeAnalyticsSerializer

    def get_queryset(self, *args, **kwargs):
        date_from = self.request.query_params.get(
            "date_from",
            (datetime.now().date() + timedelta(days=-30)).isoformat(),
        )
        date_to = self.request.query_params.get(
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

        queryset = (
            (Like.objects.filter(created_at__date__range=[date_from, date_to]))
            .values(date=F("created_at__date"))
            .order_by("-date")
            .annotate(likes_count=Count("id"))
        )

        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)

        return self.get_paginated_response(page)
