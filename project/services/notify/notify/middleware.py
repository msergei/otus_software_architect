from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication, JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


def TokenValidateMiddleware(get_response):
    def middleware(request):
        try:
            auth = JWTAuthentication()
            header = auth.get_header(request)
            raw_token = auth.get_raw_token(header)
            validated_token = auth.get_validated_token(raw_token)

            field = settings.SIMPLE_JWT['USER_ID_FIELD']
            setattr(request, field, validated_token.payload[field])
        except Exception:
            raise InvalidToken('Credentials were not provided')
        else:
            response = get_response(request)
        return response
    return middleware
