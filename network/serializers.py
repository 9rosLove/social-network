from rest_framework import serializers

from network.models import Post, Like
from user.models import User
from user.serializers import UserSerializer


class LikeSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source="created_by.__str__", read_only=True
    )

    class Meta:
        model = Like
        fields = (
            "id",
            "created_by",
        )
        read_only_fields = (
            "id",
            "created_by",
        )


class UserPostSerializer(UserSerializer):
    full_name = serializers.CharField(source="__str__", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "full_name",
        )
        read_only_fields = ("id", "full_name")


class PostSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(
        source="created_by.__str__", read_only=True
    )
    likes_count = serializers.IntegerField(
        source="likes.count", read_only=True
    )

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("created_by", "created_at")


class PostDetailSerializer(PostSerializer):
    likes = LikeSerializer(many=True, read_only=True)
    created_by = UserPostSerializer(read_only=True)
