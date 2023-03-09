from django.urls import path

from jappl_time_log.views.project.project_view import ProjectView

project_url = [
    path("", ProjectView.as_view({'get': 'list'}), name="project_root"),
    path("create/", ProjectView.as_view({'post': 'create'}), name="project_create"),
    path("delete/<int:pk>", ProjectView.as_view({'delete': 'destroy'}), name="project_delete"),
    path("update/<int:pk>", ProjectView.as_view({'patch': 'partial_update', 'put': 'update'}), name="project_update"),
]
