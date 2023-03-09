"""App JAPPL time log URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from jappl_time_log.urls.application_url import application_url
from jappl_time_log.urls.project_url import project_url
from jappl_time_log.urls.user_url import user_url

base_user_url = "user"
base_application_url = "application"
base_project_url = "project"

urlpatterns = [
    path(f"{base_user_url}/", include((user_url, "user"), namespace="user")),
    path(f"{base_project_url}/", include((project_url, "project"), namespace="project")),
    path(f"{base_application_url}/", include((application_url, "application"), namespace="application")),
]
