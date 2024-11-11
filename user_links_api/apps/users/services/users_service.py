from django.contrib.auth.hashers import make_password
from django.db.models import Q

import uuid

from ..models import User


RANDOM_USERNAME_TEMPLATE = 'user-%s'


class UsersService:
    model = User

    @classmethod
    def _get_username(cls, data):
        username = data.get('username')
        if not username:
            username = f'{data["email"]}__{str(uuid.uuid4())[:16]}'
        return username

    @classmethod
    def _encrypt_password(cls, password):
        return make_password(password)

    @classmethod
    def _build_create_params(cls, data):
        password = data['password'] if data.get('password') else cls.generate_temporary_password()[-1]
        data['password'] = cls._encrypt_password(password)
        data['username'] = cls._get_username(data)
        return data

    @classmethod
    def _build_update_params(cls, data):
        if data.get('password_confirmation'):
            data.pop('password_confirmation')

        if data.get('password'):
            data['password'] = cls._encrypt_password(data['password'])
        return data

    @classmethod
    def generate_temporary_password(cls):
        password = str(uuid.uuid4())[:8]
        return [password, cls._encrypt_password(password)]

    @classmethod
    def create(cls, data):
        create_params = cls._build_create_params(data)
        instance = cls.model.manager.create(**create_params)
        return instance

    @classmethod
    def create_by_email(cls, email, **kwargs):
        user = cls.model(email=email, **kwargs)
        user.username = email
        user.save()
        return user

    @classmethod
    def update(cls, instance, data):
        update_params = cls._build_update_params(data)

        for attr, value in update_params.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def get_by_identity(cls, identity):
        query_by_email = Q(email__iexact=identity)
        query_by_username = Q(username__iexact=identity)
        user = cls.model.manager.filter(query_by_email|query_by_username).first()
        return user

    @classmethod
    def activate(cls, data):
        user = data.pop('user')
        data['status'] = User.ACTIVE
        return cls.update(user, data)

    @classmethod
    def is_user_blocked(cls, user):
        return user and user.status in [User.BLOCKED, User.TERMINATED]

    @classmethod
    def is_user_admin(cls, user):
        return user and user.role in [User.ADMIN]
