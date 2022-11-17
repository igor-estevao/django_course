from django.urls import path
from . import views

urlpatterns = [
  path("", views.projects, name="root"),
  path("home/", views.home, name="home"),
  path("about/", views.about, name="about"),
  path("param/<str:pk>/", views.param, name="param"),
  path("projects/", views.projects, name="projects"),
  path("project/<str:pk>/", views.project, name="project"),
  path("create_project/", views.create_project, name="create_project"),
  path("update_project/<str:pk>/", views.updade_project, name="update_project"),
  path("delete_project/<str:pk>/", views.delete_project, name="delete_project"),
  path("create_review/<str:project_id>/", views.create_review, name="create_review"),
  path("update_review/<str:pk>/", views.update_review, name="update_review"),
]