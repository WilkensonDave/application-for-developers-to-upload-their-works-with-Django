from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("", views.getRoutes, name="get-routes"),
    path("projects/", views.get_projects, name="get-projects"),
    path("project/<str:pk>/", views.project, name="project"),
    path("project/<str:pk>/vote/", views.projectVote, name="projectvote"),
    path("delete-tags/", views.removeTag, name="remove-tag")
]
