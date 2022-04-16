from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework import status

import json, environ
import hmac
import hashlib

from .models import User
from .serializers import UserSerializer
from .utils import base64url_encode

env = environ.Env()
env.read_env(settings.BASE_DIR / ".env")


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response("The user doesnt exist", status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response(
            "The password is not correct.", status=status.HTTP_400_BAD_REQUEST
        )

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {"user_id": user.id}
    secret_key = env("SECRET_KEY")

    total_params = (
        str(base64url_encode(json.dumps(header)))
        + "."
        + str(base64url_encode(json.dumps(payload)))
    )
    signature = hmac.new(
        secret_key.encode(), total_params.encode(), hashlib.sha256
    ).hexdigest()
    token = total_params + "." + signature
    return Response("JWT " + token, status=status.HTTP_200_OK)


class UserList(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(RetrieveAPIView):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewset(ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
