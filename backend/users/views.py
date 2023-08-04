from django.contrib.auth import get_user_model
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAdminUser

from .serializers import CustomUserDetailsSerializer

User = get_user_model()


class UserViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CustomUserDetailsSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = (IsAdminUser,)

    # def get_queryset(self, *args, **kwargs):
    #     assert isinstance(self.request.user.id, int)
    #     if self.request.user.is_superuser:
    #         return User.objects.all()
    #     return self.queryset.filter(id=self.request.user.id)
