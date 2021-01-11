import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.forms.models import model_to_dict

from .models import User, Posts


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def create_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required." }, status=400)

    # POST request

    # load the data
    data = json.loads(request.body)
    post_text = data.get("text")

    try:

        # save new post to database
        new_post = Posts(user_id=request.user, text=post_text)
        new_post.save()
        return HttpResponse(status=204)

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Cannot create post."}, status=404)


def get_all_posts(request):

    if request.method != "GET":
        return JsonResponse({ "error": "GET request required." }, status=400)

    # GET request

    try:
        all_posts = Posts.objects.all()

        # Return posts in reverse chronologial order
        all_posts = all_posts.order_by("-date_time").all()

        # .serialize() is a method in the models
        return JsonResponse([post.serialize() for post in all_posts], safe=False, status=200)

    except Posts.DoesNotExist:
        return JsonResponse({"error": "Posts do not exist"}, status=404)


def get_user_posts(request, user_id):

    if request.method != "GET":
        return JsonResponse({ "error": "GET request required." }, status=400)

    # GET request
    try:
        # check to see if user exists
        user = User.objects.get(pk=user_id)

        # get all posts for user
        # user_posts = Posts.objects.filter(user_id=user.pk)
        user_posts = user.user_posts

        # Return posts in reverse chronologial order
        user_posts = user_posts.order_by("-date_time").all()

        # .serialize() is a method in the models
        return JsonResponse([post.serialize() for post in user_posts], safe=False, status=200)

    except Posts.DoesNotExist and User.DoesNotExist :
        return JsonResponse({"error": "User has no posts"}, status=404)


def get_user(request, user_id):

    if request.method != "GET":
        return JsonResponse({ "error": "GET request required." }, status=400)

    # GET request
    try:

        # get user model object
        user_model_object = User.objects.get(pk=user_id)

        # convert object to a dict to parse to JsonResponse
        user_dict = model_to_dict(user_model_object)

        # user_dict is serialized to JSON within the JsonResponse and returned
        return JsonResponse(user_dict, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)