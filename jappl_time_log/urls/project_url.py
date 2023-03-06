from django.urls import path

from jappl_time_log.views.project.project_view import ProjectView

project_url = [
    path("", ProjectView.as_view({'get': 'list'}), name="project"),
    path("create/", ProjectView.as_view({'post': 'create'}), name="project"),
    path("delete/<int:pk>", ProjectView.as_view({'delete': 'destroy'}), name="project"),
    path("update/<int:pk>", ProjectView.as_view({'patch': 'update', 'put': 'partial_update'}), name="project"),
]
