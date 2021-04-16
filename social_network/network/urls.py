from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

# import everything from views 
from network.views import *

# import routers and viewsets
from rest_framework import routers, viewsets

urlpatterns = [

    # API Routes
    path("create_post/", create_post, name="create_post"),
    path("all_posts/", all_posts, name="all_posts"),
    path("user_posts/<str:username>", user_posts, name="user_posts"),
    path("user/<str:username>", user, name="user"),
    path("user_followers/<str:username>", user_followers, name="user_followers"),
    path("user_following/<str:username>", user_following, name="user_following"),
    path("follow/<str:username>", follow, name="follow"),
    path("edit_post/", edit_post, name="edit_post"),
    path("like_post/<int:post_id>", like_post, name="like_post"),
    path('register_user/', register_user, name="register_user"),
    path('user_exists/<str:username>', user_exists, name='user_exists'),
    path('email_exists/<str:email>', email_exists, name='email_exists'),
    path('hello/', helloWorldView, name='helloWorldView'),
    path('get_logged_in_user/', get_logged_in_user, name='get_logged_in_user'),
    path('is_user_logged_in/', is_user_logged_in, name='is_user_logged_in'),
    path('is_following/<str:username>', is_following, name='is_following'),


    # tokens
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', logoutAndBlacklistRefreshTokenForUser, name='logoutAndBlacklistRefreshTokenForUser'),

]
