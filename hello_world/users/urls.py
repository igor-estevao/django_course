from django.urls import path
from . import views
# Create your views here.
urlpatterns = [
  path("login", views.loginUser, name="login"),
  path("logout", views.logoutUser, name="logout"),
  path("register", views.registerUser, name="register"),

  path("", views.profiles, name="profiles"),
  path("profile/<str:pk>", views.userProfile, name="profile"),
  path("account", views.userAccount, name="account"),
  path("edit_user_account", views.edit_user_account, name="edit_user_account"),

  path("create_skill", views.create_skill, name="create_skill"),
  path("edit_skill/<str:pk>", views.edit_skill, name="edit_skill"),
  path("delete_skill/<str:pk>", views.delete_skill, name="delete_skill"),

  path("inbox/", views.inbox, name="inbox"),
  path("message/<str:pk>", views.message, name="message"),
  path("send_message/<str:pk>", views.send_message, name="send_message")

]
