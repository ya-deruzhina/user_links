class AuthPayloadService:
    @classmethod
    def _get_user_payload(cls, user):
        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'status': user.status,
            'role': user.role,
            'id': user.id,
        }

    @classmethod
    def call(cls, user, token):
        return {
            'user': cls._get_user_payload(user),
            'token': token,
        }
