from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework_simplejwt.views import (
    TokenRefreshView as DjangoTokenRefreshView,
    TokenVerifyView as DjangoTokenVerifyView,
    TokenObtainPairView,
)

from user.serializers import UserSerializer


@extend_schema(tags=["User API"])
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(tags=["User API"])
class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = ()


@extend_schema(tags=["Authenticated"])
class LoginUserView(TokenObtainPairView):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


@extend_schema(tags=["Authenticated API"])
class TokenRefreshView(DjangoTokenRefreshView):
    pass


@extend_schema(tags=["Authenticated API"])
class TokenVerifyView(DjangoTokenVerifyView):
    pass
