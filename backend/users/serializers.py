from django.contrib.auth import get_user_model
from rest_framework import serializers

from backend.users.models import User as UserType


User = get_user_model()


class CustomUserDetailsSerializer(serializers.ModelSerializer[UserType]):
    emails = serializers.SerializerMethodField()

    def get_emails(self, obj: User) -> list[str]:
        print(obj._meta.fields)
        return obj.emailaddress_set.all().values_list("email", flat=True)

    class Meta:
        model = User
        fields = (
            "pk",
            "username",
            "email",
            "name",
            "emails",
        )
        read_only_fields = ("pk", "email")
