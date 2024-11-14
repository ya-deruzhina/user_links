from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

class CustomUserManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class User(AbstractUser):
    manager = CustomUserManager()

    ADMIN = 'admin'
    USER = 'user'

    USER_ROLES_CHOICES = ((ADMIN, 'Admin'), (USER, 'User'))

    WAITING_FOR_ACTIVATION = 'wfa'
    ACTIVE = 'active'
    TERMINATED = 'terminated'
    BLOCKED = 'blocked'

    USER_STATUSES = [WAITING_FOR_ACTIVATION, ACTIVE, TERMINATED, BLOCKED]

    USER_STATUSES_DESCRIPTION = [('Waiting for activation'),('Active'),('Terminated'),('Blocked')]

    USER_STATUSES_CHOICES = tuple(zip(USER_STATUSES, USER_STATUSES_DESCRIPTION))

    email = models.EmailField(unique=True, null=True)
    status = models.CharField(
        max_length=255, choices=USER_STATUSES_CHOICES, default=ACTIVE
    )
    role = models.CharField(max_length=255, choices=USER_ROLES_CHOICES, default=USER)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    last_request_at = models.DateTimeField(blank=False, null=False,auto_now=True)
    last_login_attempt_at = models.DateTimeField(auto_now=True)
    login_attempts_count = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.id}. {self.email}'

    @property
    def app_role(self):
        """
        Returns the user's role in the app.
        """
        if self.is_superuser:
            return "super_admin"
        return self.role