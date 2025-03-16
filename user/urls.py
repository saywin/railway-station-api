from django.urls import path

from user.views import ManageUserView, UserCreateView


urlpatterns = [
    path("me/", ManageUserView.as_view(), name="manage_user"),
    path("user-create/", UserCreateView.as_view(), name="user_create"),
]

app_name = "user"
