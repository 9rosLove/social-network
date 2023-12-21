from django.urls import path

from analytics.views import UserActivityView, LikeAnalyticsView

urlpatterns = [
    path("", LikeAnalyticsView.as_view()),
    path("user-activity/", UserActivityView.as_view()),
]
