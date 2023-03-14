from django.urls import path

from jappl_time_log.views.project_member.project_member_view import ProjectMemberViewSet

project_member_url = [
    path("list", ProjectMemberViewSet.as_view({'get': 'list'}), name="list"),
    path("detail/<int:project_member_id>", ProjectMemberViewSet.as_view({'get': 'retrieve'}), name="detail"),
    path("add", ProjectMemberViewSet.as_view({'post': 'create'}), name="add"),
    path("delete/<int:project_member_id>", ProjectMemberViewSet.as_view({'delete': 'destroy'}), name="delete"),
    path(
        "update/<int:project_member_id>",
        ProjectMemberViewSet.as_view({'patch': 'partial_update', 'put': 'update'}),
        name="update",
    ),
]
