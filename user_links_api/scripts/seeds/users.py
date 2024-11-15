from apps.users.models import User
from apps.users.services import UsersService
from faker import Faker
fake = Faker()


def get_users_params(user_email):
    return {
        "email": user_email,
        "password": "password",
    }


def perform(*args, **kwargs):
    if len(User.objects.all()) == 0:
        for n in range(5):
            user_email = fake.email()
            if not User.objects.filter(email=user_email).exists():
                UsersService.create(get_users_params(user_email))
    if not User.objects.filter(email='userka@user.com').exists():
        UsersService.create(get_users_params('userka@user.com'))
