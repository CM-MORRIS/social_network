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
    path("get_user/<int:user_id>", views.get_user, name="get_user")

]
