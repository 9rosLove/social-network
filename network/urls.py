from rest_framework.routers import DefaultRouter

from network.views import PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet)

urlpatterns = router.urls

app_name = "network"
