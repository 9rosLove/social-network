from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from network.models import Post, Like
from network.pagination import PostPagination
from network.permissions import IsOwnerOrReadOnly
from network.serializers import (
    PostSerializer,
    LikeSerializer,
    PostDetailSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "updated_at"]
    search_fields = ["title", "content"]

    def get_serializer_class(self):
        if self.action in ["like", "unlike"]:
            return LikeSerializer
        if self.action == "retrieve":
            return PostDetailSerializer

        return super().get_serializer_class()

    @action(
        methods=["POST"],
        detail=True,
        url_path="like",
        permission_classes=[IsAuthenticated],
    )
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        like_ = Like.objects.filter(post=post, created_by=user)

        if like_.exists():
            return Response(
                {"error": "You have already liked this post."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Like.objects.create(post=post, created_by=user)

        return Response({"detail": "Post liked successfully."}, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="unlike",
        permission_classes=[IsAuthenticated],
    )
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like_to_delete = Like.objects.filter(post=post, created_by=user)

        if like_to_delete.exists():
            like_to_delete.delete()
            return Response({"detail": "Post unliked successfully."}, status.HTTP_200_OK)

        return Response({"error": "You have not liked this post yet."}, status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
