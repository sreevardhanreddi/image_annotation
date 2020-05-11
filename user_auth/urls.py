from django.urls import path, re_path
from user_auth.views import (
    # index,
    user_profile,
    user_login,
    user_logout,
    user_register,
)

app_name = "user_auth"

urlpatterns = [
    # path("", index, name="index"),
    path("login/", user_login, name="user_login"),
    path("register/", user_register, name="user_register"),
    path("profile/", user_profile, name="user_profile"),
    path("logout/", user_logout, name="user_logout"),
]
