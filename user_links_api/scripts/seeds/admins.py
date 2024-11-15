from apps.users.models import User
from apps.users.services import UsersService


def get_admins_params():
    return {
        "username": "admin",
        "email": "admin@admin.admin",
        "password": "admin",
        "status": User.ACTIVE,
        "is_superuser": True,
        "role": User.ADMIN,
        "is_staff": True,
    }


def perform(*args, **kwargs):
    if not User.objects.filter(username="admin").exists():
        UsersService.create(get_admins_params())
