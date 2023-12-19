from django.urls import path

from analytics.views import UserActivityView, AnalyticsView

urlpatterns = [
    path("", AnalyticsView.as_view()),
    path("user-activity/", UserActivityView.as_view())
]
