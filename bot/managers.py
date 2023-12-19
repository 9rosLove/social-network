import asyncio

import urls
from models import Post, User

import httpx
from faker import Faker

faker = Faker()


class UserManager:
    def __init__(self, semaphore: asyncio.Semaphore):
        self.semaphore = semaphore
        self.users = []

    async def register_user(self, user: User, client: httpx.AsyncClient) -> httpx.Response:
        async with self.semaphore:
            response = await client.post(urls.REGISTER_URL, data=user.__dict__)

            if response.status_code == 400 and response.json()["email"][0] == "user with this email address already exists.":
                print("User already exists")
                user.email = faker.email()
                return await self.register_user(user, client)

        return response

    async def obtain_jwt(self, user: User, client: httpx.AsyncClient) -> httpx.Response:
        async with self.semaphore:
            response = await client.post(urls.OBTAIN_JWT_URL, data=user.__dict__)
            if response.status_code == 200:
                user.update_token(response.json()["access"])

        return response


class PostManager:
    def __init__(self, semaphore: asyncio.Semaphore):
        self.post_ids = []
        self.semaphore = semaphore

    async def create_post(self, client: httpx.AsyncClient,  post: Post, headers: dict) -> httpx.Response:

        async with self.semaphore:
            response = await client.post(
                urls.POST_URL, headers=headers, data=post.__dict__
            )
        return response

    async def like_post(self, client: httpx.AsyncClient, post_id: int, headers: dict) -> httpx.Response:
        url = f"{urls.BASE_URL}network/posts/{post_id}/like/"

        async with self.semaphore:
            response = await client.post(
                url, headers=headers
            )
        return response
