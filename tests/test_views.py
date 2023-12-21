from datetime import datetime

from django.contrib.auth import get_user_model

from network.models import Post
from user.models import User

from django.test import TestCase
from rest_framework.test import APIClient

BASE_URL = "http://127.0.0.1:8000/api/"
REGISTER_URL = f"{BASE_URL}user/register/"
OBTAIN_JWT_URL = f"{BASE_URL}user/token/"
POST_URL = f"{BASE_URL}network/posts/"
ANALYTICS_URL = f"{BASE_URL}analytics/"


def post_reaction(action: str, post_id: int):
    return f"{BASE_URL}network/posts/{post_id}/{action}/"


class TestUnauthenticated(TestCase):
    def test_create_post_authentication_required(self):
        data = {"title": "Test Post", "content": "Test Content"}
        response = self.client.post(POST_URL, data=data)

        self.assertEqual(response.status_code, 401)

    def test_user_activity_authentication_required(self):
        url = f"{ANALYTICS_URL}user-activity/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_like_post_authentication_required(self):
        user = get_user_model().objects.create_user(
            email="test@test",
            password="test",
            first_name="test",
            last_name="test",
        )
        Post.objects.create(
            title="Test Post", content="Test Content", created_by=user
        )
        url = f"{BASE_URL}network/posts/1/like/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, 401)


class TestAuthenticated(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test",
            password="test",
            first_name="test",
            last_name="test",
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", created_by=self.user
        )

    def test_create_post(self):
        data = {"title": "Test Post", "content": "Test Content"}
        response = self.client.post(POST_URL, data=data)

        self.assertEqual(response.status_code, 201)

    def test_analytics(self):
        like_url = post_reaction("like", self.post.id)
        self.client.post(like_url)
        current_date = datetime.now().strftime("%Y-%m-%d")
        response = self.client.get(ANALYTICS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {"date": current_date, "likes_count": 1},
            ],
        )

    def test_like_post_single_time(self):
        url = f"{BASE_URL}network/posts/{self.user.posts.first().id}/like/"
        response = self.client.post(url)
        print(self.user.is_authenticated)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"detail": "Post liked successfully."}
        )

    def test_unlike_post(self):
        like_url = post_reaction("like", self.post.id)
        unlike_url = post_reaction("unlike", self.post.id)
        self.client.post(like_url)
        response = self.client.post(unlike_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"detail": "Post unliked successfully."}
        )

    def test_unlike_post_like_not_exist(self):
        url = post_reaction("unlike", self.post.id)
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"error": "You have not liked this post yet."}
        )

    def test_like_post_already_liked(self):
        url = post_reaction("like", self.post.id)
        self.client.post(url)
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), {"error": "You have already liked this post."}
        )


class TestIsOwnerOrReadOnly(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@test",
            password="test",
            first_name="test",
            last_name="test",
        )
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", created_by=self.user
        )

    def test_update_post(self):
        data = {"title": "Test Post", "content": "Test Content"}
        url = f"{POST_URL}{self.post.id}/"
        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, 200)

    def test_update_post_not_owner(self):
        data = {"title": "Test Post", "content": "Test Content"}
        user = User.objects.create_user(
            email="test2@test",
            password="test",
            first_name="test",
            last_name="test",
        )
        post = Post.objects.create(
            title="Test Post", content="Test Content", created_by=user
        )
        url = f"{POST_URL}{post.id}/"
        response = self.client.put(url, data=data)

        self.assertEqual(response.status_code, 403)
