from django.urls import path

from user.views import (
    ManageUserView,
    UserCreateView,
    LoginUserView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path("me/", ManageUserView.as_view(), name="manage_user"),
    path("user-create/", UserCreateView.as_view(), name="user_create"),
    path("token/", LoginUserView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("verify/", TokenVerifyView.as_view(), name="token_verify"),
]

app_name = "user"
