from faker import Faker


class User:
    faker = Faker()

    def __init__(self):
        self.first_name = self.faker.first_name()
        self.last_name = self.faker.last_name()
        self.email = self.faker.email()
        self.password = self.faker.password()
        self.access_token = None

    def update_token(self, token):
        self.access_token = token

    def __str__(self):
        return self.email


class Post:
    faker = Faker()

    def __init__(self):
        self.title = self.faker.sentence()
        self.content = self.faker.text()

    def __str__(self):
        return self.title
