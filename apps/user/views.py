# Vendor
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group

# Local
from apps.utils.exceptions import CustomException
from django.conf import settings
from . import models
from . import serializers
from apps.user.register.utils import generate_token
from .serializers import GroupSerializer
from ..utils.classes import Pagination


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

@api_view(['GET'])
def get_profile(request):
    if request.user.id:
        data = models.User.objects.filter(id=request.user.id).last()
        return Response(serializers.UserProfileSerializer(data).data)
    raise CustomException(translate_code="not_authorised")


class MyPermissionGroupsView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    pagination_class = Pagination
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        my_groups = user.groups.all()
        return Response(GroupSerializer(my_groups, many=True).data)


class TokenRefreshView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer

    def create(self, request, *args, **kwargs):
        from apps.user.register.utils import verify_token
        """Обновление токена - возвращаем access, refresh """

        refresh = request.data.get("refresh", "")
        if refresh:
            verified_token = verify_token(refresh, 'refresh')
            if verified_token:
                user = models.User.objects.filter(id=verified_token['user_id']).last()

                if user and user.is_active:
                    access = generate_token(
                        user,
                        settings.JWT_ACCESS_TOKEN_LIFETIME,
                    )
                    new_refresh = generate_token(
                        user,
                        settings.JWT_REFRESH_TOKEN_LIFETIME,
                        'refresh'
                    )
                    return Response({'access': access,
                                     'refresh': new_refresh
                                     })
                print("auth error 5")
                raise CustomException(
                    translate_code="user_inactive_or_deleted_4",
                    code=status.HTTP_403_FORBIDDEN
                )
        raise CustomException(translate_code="session_time_expired", code=status.HTTP_403_FORBIDDEN)
