from django.urls import path
from . import views


urlpatterns = [
    path("", views.projects, name="projects"),
    path("single-project/<str:pk>", views.single_project, name="single-project"),
    path("create-project/", views.createProject, name="create-project"),
    path("updateproject/<str:pk>/", views.updateproject, name="updateproject"),
    path("deleteproject/<str:pk>/", views.deleteproject, name="delete-project"),
]
