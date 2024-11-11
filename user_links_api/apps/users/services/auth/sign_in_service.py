from django.contrib.auth.models import update_last_login

from datetime import datetime, timezone

from .jwt_token_service import JWTTokenService


class SignInService:
    @classmethod
    def login(cls, request, user):
        token = JWTTokenService.generate(user)
        user.last_request_at = datetime.now(timezone.utc)
        user.save()
        update_last_login(request, user)
        return token

    @classmethod
    def limited_login(cls, request, user):
        token = JWTTokenService.generate(user)
        update_last_login(request, user)
        return token
