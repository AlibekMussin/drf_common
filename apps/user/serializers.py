# Vendor
from rest_framework import serializers

# Local
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=300,
        required=True
    )
    password = serializers.CharField(
        max_length=128,
        required=True
    )

    class Meta:
        fields = (
            'username',
            'password',
        )
        model = User
