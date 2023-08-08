from django.contrib.auth import get_user_model
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomUserDetailsSerializer

User = get_user_model()


class UserViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CustomUserDetailsSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = (IsAdminUser,)
