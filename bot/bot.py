import asyncio
import logging
import random

from managers import UserManager, PostManager
from utils import read_config, parse_args, write_to_csv
from models import User, Post

from faker import Faker
import httpx

faker = Faker()


class NetworkActivityBot:
    def __init__(self, user_manager: UserManager, post_manager: PostManager):
        self.user_manager = user_manager
        self.post_manager = post_manager

    async def register_users(
        self, client: httpx.AsyncClient, number_of_users: int
    ) -> None:
        """Creates a random number of fake users"""
        self.user_manager.users.extend(
            [User() for _ in range(number_of_users)]
        )

        tasks = [
            self.user_manager.register_user(user=user, client=client)
            for user in self.user_manager.users
        ]
        await asyncio.gather(*tasks)

    async def obtain_jwts(self, client: httpx.AsyncClient) -> None:
        """Obtains JWT tokens for each user"""
        tasks = [
            self.user_manager.obtain_jwt(user, client)
            for user in self.user_manager.users
        ]
        await asyncio.gather(*tasks)

    async def create_posts(
        self, client: httpx.AsyncClient, max_posts_per_user: int
    ) -> None:
        """Creates a random number of random posts for each user"""
        tasks = []

        for user in self.user_manager.users:
            posts_number = random.randint(1, max_posts_per_user)
            headers = {"Authorization": f"Bearer {user.access_token}"}

            for _ in range(posts_number):
                post = Post()
                tasks.append(
                    asyncio.create_task(
                        self.post_manager.create_post(client, post, headers)
                    )
                )

        posts = await asyncio.gather(*tasks)

        for post in posts:
            self.post_manager.post_ids.append(post.json()["id"])

    async def like_posts(
        self, client: httpx.AsyncClient, max_likes_per_user: int
    ) -> None:
        """Likes a random number of random posts for each user"""
        tasks = []

        for user in self.user_manager.users:
            likes_number = random.randint(0, max_likes_per_user)
            headers = {"Authorization": f"Bearer {user.access_token}"}

            for _ in range(likes_number):
                post_id = random.choice(self.post_manager.post_ids)
                tasks.append(
                    asyncio.create_task(
                        self.post_manager.like_post(client, post_id, headers)
                    )
                )

        await asyncio.gather(*tasks)


async def start():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    args = parse_args()
    config = read_config(args.config)

    number_of_users = config.get("number_of_users", 10)
    max_posts_per_user = config.get("max_posts_per_user", 10)
    max_likes_per_user = config.get("max_likes_per_user", 10)
    semaphore_value = config.get("semaphore_value", 10)

    semaphore = asyncio.BoundedSemaphore(semaphore_value)
    user_manager = UserManager(semaphore)
    post_manager = PostManager(semaphore)
    bot = NetworkActivityBot(user_manager, post_manager)

    async with httpx.AsyncClient() as client:
        await bot.register_users(client, number_of_users)
        await bot.obtain_jwts(client)
        await bot.create_posts(client, max_posts_per_user)
        await bot.like_posts(client, max_likes_per_user)

    if args.output:
        logging.info("Writing results to %s", args.output)
        write_to_csv(users=bot.user_manager.users, file_path=args.output)

    logging.info("Done!")


if __name__ == "__main__":
    asyncio.run(start())
