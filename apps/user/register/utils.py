import jwt
import re
import random
import string
from datetime import datetime, timezone

from django.conf import settings
from project import settings


def generate_auth_hash():
    letters = string.ascii_lowercase + '0123456789'
    session_hash = ''.join(random.choice(letters) for i in range(12))
    return session_hash


def verify_token(token, token_type='access'):
    """Проверка токена"""
    try:
        decoded_jwt = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=(settings.JWT_ALGORITHM,)
        )
    except:
        return None

    if decoded_jwt['token_type'] != token_type:
        return None

    return decoded_jwt


def generate_token(user, exp_time, token_type='access'):
    """
    Генерируем ресет токен для сброса пароля
    :param user: объект класса User (app.models)
    :param exp_time: срок токена в datetime.timedelta
    :param token_type: тип токена
    """
    expire_date = round((datetime.now(tz=timezone.utc) + exp_time).timestamp())
    person = user.person.last()
    first_name = ""
    last_name = ""
    session_hash: str = ""
    if person:
        first_name = person.first_name
        last_name = person.last_name

    if token_type == 'access':
        session_hash = generate_auth_hash()
        user.session_hash = session_hash
        user.save()
    body = {
        'token_type': token_type,
        'exp': expire_date,
        'user_id': user.id,
        'first_name': first_name,
        'last_name': last_name
    }
    if token_type == 'access':
        body['session_hash'] = session_hash
    elif token_type == 'refresh':
        body['session_hash'] = user.session_hash
    encoded_body = jwt.encode(
        body,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_body
