from django.urls import path

from analytics.views import UserActivityView

urlpatterns = [
    path("user-activity/", UserActivityView.as_view()),
]
