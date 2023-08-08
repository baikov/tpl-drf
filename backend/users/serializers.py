from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.users.models import User as UserType

User = get_user_model()


class CustomUserDetailsSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "email",
            "name",
        )
        read_only_fields = ("pk", "email")
