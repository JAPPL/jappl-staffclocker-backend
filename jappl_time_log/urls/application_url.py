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
    path("permission/list", ApplicationPermissionViewSet.as_view({'get': 'list'}), name="permission-list"),
    path("permission/add", ApplicationPermissionViewSet.as_view({'post': 'create'}), name="permission-add"),
    path(
        "permission/update/<application_permission_id>",
        ApplicationPermissionViewSet.as_view({'put': 'update', 'patch': 'partial_update'}),
        name="permission-update",
    ),
    path(
        "permission/delete/<int:application_permission_id>",
        ApplicationPermissionViewSet.as_view({'delete': 'destroy'}),
        name="permission-delete",
    ),
    path(
        "permission/detail/<int:application_permission_id>",
        ApplicationPermissionViewSet.as_view({'get': 'retrieve'}),
        name="permission-detail",
    ),
]
