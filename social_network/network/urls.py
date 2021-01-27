from django.urls import path, include

# import everything from views 
from network.views import *

# import routers and viewsets
from rest_framework import routers, viewsets

urlpatterns = [

    path("", index, name="index"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),

    # API Routes
    path("create_post", create_post, name="create_post"),
    path("all_posts", all_posts, name="all_posts"),
    path("user_posts/<str:user_id>", user_posts, name="user_posts"),
    path("user/<str:username>", user, name="user"),
    path("user_followers/<str:user_id>", user_followers, name="user_followers"),
    path("user_following/<str:user_id>", user_following, name="user_following"),
    path("follow/<str:user_id>", follow, name="follow"),
    path("edit_post", edit_post, name="edit_post"),
    path("like_post/<int:post_id>", like_post, name="like_post")

]
