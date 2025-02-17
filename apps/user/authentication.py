# Vendor
import hmac

from rest_framework.authentication import get_authorization_header
from rest_framework import authentication, exceptions
from rest_framework import status
from django.conf import settings

# Local
from apps.user.models import User
from apps.utils.exceptions import CustomException


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        """Аутентификация JWT-токена
        """
        auth = get_authorization_header(request).split()
        if len(auth) > 1:
            try:
                from apps.user.register.utils import verify_token

                if 'refresh' in request.data:
                    token_type = 'refresh'
                    token = request.data.get('refresh', '')
                else:
                    token_type = 'access'
                    token = auth[1].decode()

                body = verify_token(token, token_type)
                if not body:
                    raise CustomException(translate_code="invalid_token_2", code=status.HTTP_403_FORBIDDEN)

            except UnicodeError:
                raise CustomException(translate_code="invalid_token_header", code=status.HTTP_400_BAD_REQUEST)
            session_hash = body.get('session_hash', None)
            return self.authenticate_credentials(body=body, session_hash=session_hash)

    def authenticate_credentials(self, body, session_hash=''):
        """Проверка наличия активного пользователя
        """
        user_id = body.get('user_id', None)
        if user_id:
            user = User.objects.get(id=user_id)
            if user is None:
                # User doesnt exist
                raise CustomException(translate_code="wrong_password_or_username", code=status.HTTP_403_FORBIDDEN)
            if settings.SESSION_HASH_ENABLED and session_hash:
                self.compare_auth_hash(
                    hash_from_user=session_hash,
                    users_hash=user.session_hash)

            if not user.is_active:
                raise CustomException(translate_code="user_inactive", code=status.HTTP_403_FORBIDDEN)
            return (user, None)
        raise CustomException(translate_code="invalid_token_4", code=status.HTTP_403_FORBIDDEN)

    def compare_auth_hash(self, hash_from_user, users_hash):
        if hmac.compare_digest(hash_from_user, users_hash):
            return True
        else:
            raise CustomException(translate_code="two_chairs_exception", code=status.HTTP_401_UNAUTHORIZED)
