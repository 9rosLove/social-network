import datetime

from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )

    def __str__(self):
        short_content = self.content[:50]
        return (
            short_content + "..." if len(self.content) > 50 else self.content
        )


class Like(models.Model):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        unique_together = (("post", "created_by"),)

    def __str__(self):
        return f"{self.created_by} - {self.post}"
