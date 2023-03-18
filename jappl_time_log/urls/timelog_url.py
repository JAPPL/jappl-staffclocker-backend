from django.urls import path

from jappl_time_log.views.timelog.timelog_approve_view import TimeLogApproveView
from jappl_time_log.views.timelog.timelog_list_all_view import TimeLogListAllView
from jappl_time_log.views.timelog.timelog_view import TimeLogView

timelog_url = [
    path("", TimeLogView.as_view({'get': 'list'}), name="timelog_root"),
    path("create", TimeLogView.as_view({'post': 'create'}), name="timelog_create"),
    path("delete/<int:pk>", TimeLogView.as_view({'delete': 'destroy'}), name="timelog_delete"),
    path("update/<int:pk>", TimeLogView.as_view({'patch': 'partial_update', 'put': 'update'}), name="timelog_update"),
    path("all", TimeLogListAllView.as_view(), name="timelog_list_all"),
    path("approve/<int:pk>", TimeLogApproveView.as_view(), name="timelog_approve"),
]
