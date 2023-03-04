from django.urls import path

from jappl_time_log.views.user.login_view import LoginView

user_url = [path("login/", LoginView.as_view(), name="login")]
