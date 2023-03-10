from django.urls import path

from jappl_time_log.views.user.login_view import LoginView
from jappl_time_log.views.user.register_view import RegisterView
from jappl_time_log.views.user.user_detail_view import UserDetailView
from jappl_time_log.views.user.user_edit_view import UserEditView
from jappl_time_log.views.user.user_list_view import UserListView

user_url = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
    path("list", UserListView.as_view(), name="list"),
    path("detail/<int:user_id>", UserDetailView.as_view(), name="detail"),
    path("update/<int:user_id>", UserEditView.as_view(), name="update"),
]
