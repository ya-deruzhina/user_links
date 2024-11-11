from datetime import datetime, timedelta, timezone

from rest_framework.serializers import CharField, Serializer, ValidationError

from django.conf import settings
from ..errors import INVALID_CREDENTIALS_ERROR, INVALID_CREDENTIALS_BLOCKED_ERROR
from ..services import UsersService


class SignInSerializer(Serializer):
    identity = CharField()
    password = CharField()

    def validate(self, attrs):
        identity = attrs['identity']
        user = UsersService.get_by_identity(identity)

        if user:
            if UsersService.is_user_admin(user) and user.login_attempts_count == settings.ADMIN_MAX_LOGIN_ATTEMPTS:
                if datetime.now(timezone.utc) - user.last_login_attempt_at > timedelta(
                    minutes=settings.ADMIN_NEW_LOGIN_TIMEOUT_MINUTES
                ):
                    user.login_attempts_count = 0
                    user.save()
                else:
                    raise ValidationError(INVALID_CREDENTIALS_BLOCKED_ERROR)

            if not user.check_password(attrs['password']):
                user.last_login_attempt_at = datetime.now(timezone.utc)
                user.login_attempts_count += 1
                user.save()
                raise ValidationError(INVALID_CREDENTIALS_ERROR)

            user.login_attempts_count = 0
            user.save()
        else:
            raise ValidationError(INVALID_CREDENTIALS_ERROR)
        attrs.update({"user": user})

        return attrs
