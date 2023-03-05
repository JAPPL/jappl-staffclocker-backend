from django.urls import path

from jappl_time_log.views.user.login_view import LoginView
from jappl_time_log.views.user.register_view import RegisterView

user_url = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
]
