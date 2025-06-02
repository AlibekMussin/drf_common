# Vendor
from rest_framework import serializers
from django.contrib.auth.models import Group

# Local
from .models import User, Person


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

class PersonFullSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Person


class UserProfileSerializer(serializers.ModelSerializer):
    person = PersonFullSerializer(many=True)

    class Meta:
        fields = ['id', 'username', 'email', 'person', 'region']
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("id", 'username', 'email')
        model = User