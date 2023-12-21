from rest_framework import serializers


class LikeAnalyticsSerializer(serializers.Serializer):
    date = serializers.DateField()
    likes_count = serializers.IntegerField()

