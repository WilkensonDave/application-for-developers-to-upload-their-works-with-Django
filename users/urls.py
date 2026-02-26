from django.urls import path
from . import views

urlpatterns = [
    path("", views.profiles, name="profiles"),
    path("user-profile/<str:pk>/", views.userprofile, name="userprofile"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("account/", views.userAccount, name="account"),
    path("editaccount/", views.editAccount, name="editaccount"),
    path("createskills/", views.createSkills, name="createskills"),
    path("deleteskill/<str:pk>/", views.delete_skills, name="deleteskill"),
    path("updateskill/<str:pk>/", views.updateSkills, name="updateskill"),
    path("inbox/", views.inbox, name="inbox"),
    path("message/<str:pk>/", views.viewMessage, name="message"),
    path("sendmessage/<str:pk>", views.sendMessage, name="sendmessage")
]
