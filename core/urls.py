from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("users", views.UserViewset, basename="users")


urlpatterns = [
    # path("jwt/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
    path("login/", views.login, name="login"),
]
