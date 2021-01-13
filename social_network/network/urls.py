from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("create_post", views.create_post, name="create_post"),
    path("all_posts", views.get_all_posts, name="get_all_posts"),
    path("get_user_posts/<str:username>", views.get_user_posts, name="get_user_posts"),
    path("get_user_details/<str:username>", views.get_user_details, name="get_user_details"),
    path("get_user_followers/<str:username>", views.get_user_followers, name="get_user_followers"),
    path("get_user_following/<str:username>", views.get_user_following, name="get_user_following"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("edit_post", views.edit_post, name="edit_post")



]
