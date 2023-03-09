from django.urls import path

from jappl_time_log.views.application.application_permission_view import ApplicationPermissionViewSet
from jappl_time_log.views.application.application_view import ApplicationViewSet

application_url = [
    path("list", ApplicationViewSet.as_view({'get': 'list'}), name="list"),
    path("add", ApplicationViewSet.as_view({'post': 'create'}), name="add"),
    path("detail/<int:application_id>", ApplicationViewSet.as_view({'get': 'retrieve'}), name="detail"),
    path(
        "update/<int:application_id>",
        ApplicationViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
        name="update",
    ),
    path("delete/<int:application_id>", ApplicationViewSet.as_view({'delete': 'destroy'}), name="delete"),
    path("member/list", ApplicationPermissionViewSet.as_view({'get': 'list'}), name="member-list"),
    path("member/add", ApplicationPermissionViewSet.as_view({'post': 'create'}), name="member-add"),
    path(
        "member/update",
        ApplicationPermissionViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
        name="member-update",
    ),
    path(
        "member/delete/<int:application_permission_id>",
        ApplicationPermissionViewSet.as_view({'delete': 'destroy'}),
        name="member-delete",
    ),
    path(
        "member/detail/<int:application_permission_id>",
        ApplicationPermissionViewSet.as_view({'get': 'retrieve'}),
        name="member-detail",
    ),
]
