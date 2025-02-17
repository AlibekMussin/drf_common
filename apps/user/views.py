# Vendor
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate

from apps.utils.exceptions import CustomException
from django.conf import settings
from . import models
from . import serializers
from apps.user.register.utils import generate_token


class LoginByEmailView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = ()

    def create(self, request, *args, **kwargs):
        """Авторизация по email - возвращает токен"""
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            raise CustomException(translate_code="no_username_or_password")

        username = serializer.data.get('username')
        password = serializer.data.get('password')

        check_blocked = models.User.objects.filter(
            username=username,
            is_blocked=True
        ).last()
        if check_blocked:
            raise CustomException(translate_code="you_are_blocked")

        user = authenticate(request=request,
                            username=username,
                            password=password)

        if user:
            if user.is_blocked:
                raise CustomException(translate_code="user_is_blocked")
            if user.is_active:
                access = generate_token(
                    user,
                    settings.JWT_ACCESS_TOKEN_LIFETIME,
                )
                refresh = generate_token(
                    user,
                    settings.JWT_REFRESH_TOKEN_LIFETIME,
                    'refresh'
                )
                return Response({'access': access, 'refresh': refresh})
            else:
                raise CustomException(
                    translate_code="user_inactive",
                    code=status.HTTP_400_BAD_REQUEST
                )
        else:
            raise CustomException(
                translate_code="wrong_username_or_password",
                code=status.HTTP_401_UNAUTHORIZED
            )
