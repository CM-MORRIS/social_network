import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Posts, Follows, Likes


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

    # load the data
    data = json.loads(request.body)
    post_text = data.get("text")

    try:

        # save new post to database
        new_post = Posts(user_id=request.user, text=post_text)
        new_post.save()
        return JsonResponse({"message": "Post created"}, status=201)

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

#@login_required
def get_user_posts(request, username):

    if request.method != "GET":
        return JsonResponse({ "error": "GET request required." }, status=400)

    # GET request
    try:
        # check to see if user exists
        user = User.objects.get(username=username)

        # get all posts for user
        # user_posts = Posts.objects.filter(user_id=user.pk)
        user_posts = user.user_posts

        # Return posts in reverse chronologial order
        user_posts = user_posts.order_by("-date_time").all()

        # .serialize() is a method in the models
        return JsonResponse([post.serialize() for post in user_posts], safe=False, status=200)

    except Posts.DoesNotExist and User.DoesNotExist:
        return JsonResponse({"error": "User has no posts"}, status=404)


def get_user_details(request, username):

    if request.method != "GET":
        return JsonResponse({ "error": "GET request required." }, status=400)

    # GET request
    try:

        user_obj = User.objects.get(username=username)

        return JsonResponse(user_obj.serialize(), status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

#@login_required
def get_user_followers(request, username):

    if request.method != "GET":
        return JsonResponse({ "error": "GET request required." }, status=400)

    try:

        user = User.objects.get(username=username)

        followers = user.user_followed_by

        # have to use the .all() for iterable to work
        return JsonResponse([follower.serialize() for follower in followers.all()],
                                safe=False, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)

#@login_required
def get_user_following(request, username):

    if request.method != "GET":
        return JsonResponse({ "error": "GET request required." }, status=400)

    try:
        user = User.objects.get(username=username)

        followings = user.user_follows

        return JsonResponse([follower.serialize() for follower in followings.all()], safe=False, status=200)

    except User.DoesNotExist:
        return JsonResponse({"error": "User does not exist"}, status=404)


@login_required
def follow(request, username):
    
    if (request.method != "POST"):
        return JsonResponse({ "error": "POST request required." }, status=400)

    if (request.user.username == username):
        return JsonResponse({ "message": "Cannot follow self" }, status=404)

    try:
        user_to_follow = User.objects.get(username=username)

        obj, created = Follows.objects.get_or_create(
            user_id=request.user, user_following=user_to_follow
        )

        # if already exists, invert the boolean (i.e. follow and unfollow)
        if not created:
            bool_value = obj.isFollowing
            obj.isFollowing = not bool_value
            obj.save()
            return JsonResponse({ "message": "Updated follow status" }, status=200)
        
        return JsonResponse({ "message": "Created new follow" }, status=201)

    except User.DoesNotExist: # what if multiple rows retruned to get?
        return JsonResponse({ "error": "User does not exist." }, status=404)

@login_required
def edit_post(request):

    if (request.method != "PUT"):
        return JsonResponse({ "error": "PUT request required." }, status=400)
    
    # load the data
    data = json.loads(request.body)
    post_id = data.get("post_id")
    post_text = data.get("text")

    try:
        # get post wanting to edit, must match logged in users own post
        post = Posts.objects.get(pk=post_id, user_id=request.user)

        # update text
        post.text = post_text
        post.save()
        return JsonResponse({"message": "Post updated"}, status=200)
        
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)


@login_required
def like_post(request, post_id):

    if (request.method != "PUT"):
        return JsonResponse({ "error": "PUT request required." }, status=400)
    
    try:
        # get the post to like/unlike
        post = Posts.objects.get(pk=post_id)

        # create a new like entry, or just get the row if already exists
        obj, created = Likes.objects.get_or_create(
            user_id=request.user, post_id=post
        )

        # if already exists, invert the boolean (i.e. like (True) and unlike (False))
        if not created:
            bool_value = obj.is_liked
            obj.is_liked = not bool_value
            obj.save()

            # increase/decrease post like count
            if (obj.is_liked):
                post.like()
            else:
                post.unlike()

            return JsonResponse({ "message": "Updated liked status" }, status=200)
        
        # increase like count on post on newly created like
        post.like()
        
        # if user has never liked post before, create new record with default being liked (True)
        return JsonResponse({ "message": "Created new like" }, status=201)
        
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
