import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, get_connection
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .serializers import CustomUserDetailsSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


class UserViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CustomUserDetailsSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    permission_classes = (IsAdminUser,)


class MailView(APIView):
    def post(self, request):
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        ) as connection:
            subject = "Test Email"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [
                request.data.get("email"),
            ]
            message = "This is a test email"
            try:
                EmailMessage(
                    subject, message, email_from, recipient_list, connection=connection
                ).send()
                return Response("OK", status=200)
            except Exception as e:
                logger.error(e)

        return Response("Bad", status=400)
