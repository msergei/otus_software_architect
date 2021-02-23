from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.state import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthenticationWithCreate(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken('Token contained no recognizable user identification')

        user, created = User.objects.get_or_create(**{api_settings.USER_ID_FIELD: user_id})

        if not user.is_active:
            raise AuthenticationFailed('User is inactive', code='user_inactive')

        return user
