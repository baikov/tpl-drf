from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from backend.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()  # type: ignore

router.register("", UserViewSet)

app_name = "users"
urlpatterns = router.urls
