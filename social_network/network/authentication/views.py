from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
import json
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response 
from django.shortcuts import get_object_or_404

from .models import User, Posts, Follows, Likes
from network.serializers import PostsSerializer, UserSerializer, FollowsSerializer, LikesSerializer



from .serializers import MyTokenObtainPairSerializer, CustomUserSerializer

class ObtainTokenPairWithColorView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class HelloWorldView(APIView):

    def get(self, request):
        return Response(data={"hello":"world"}, status=status.HTTP_200_OK)


def index(request):
    return render(request, "network/all_posts.html")


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


@permission_classes(IsAuthenticated)
@api_view(['GET'])
def user(request, username):

    user = User.objects.get(username=username)
    serializer = UserSerializer(user, many=False)

    return JsonResponse(serializer.data, status=200)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def all_posts(request):

    # get all posts ordered by date ascending
    all_posts = Posts.objects.order_by("-date_time").all()
    serializer = PostsSerializer(all_posts, many=True)

    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):

    # load the data
    data = json.loads(request.body)
    post_text = data.get("text")

    data = {
        "user_id": request.user.pk,
        "text": post_text
    }

    serializer = PostsSerializer(data=data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()

        return JsonResponse({"message": "Post created"}, status=201)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_posts(request, user_id):

    user_posts = Posts.objects.order_by("-date_time").filter(user_id=user_id)
    serializer = PostsSerializer(user_posts, many=True)

    return JsonResponse(serializer.data, status=200, safe=False)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_followers(request, user_id):

    user = get_object_or_404(User, pk=user_id)
    followers = user.user_followed_by
    serializer = FollowsSerializer(followers, many=True)

    return JsonResponse(serializer.data, status=200, safe=False)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def user_following(request, user_id):

    user = get_object_or_404(User, pk=user_id)
    follows = user.user_follows
    serializer = FollowsSerializer(follows, many=True)
    return JsonResponse(serializer.data, status=200, safe=False)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def follow(request, user_id):
    
    user_to_follow = get_object_or_404(User, pk=user_id)

    if (request.user.pk == user_id):
        return JsonResponse({ "message": "Cannot follow self" }, status=404)


    obj, created = Follows.objects.get_or_create(
        user_id=request.user, user_following=user_to_follow
    )

    # if already exists, invert the boolean (i.e. follow and unfollow)
    if not created:
        bool_value = obj.is_following
        obj.is_following = not bool_value
        obj.save()
        return JsonResponse({ "message": "Updated follow status" }, status=200)
    
    return JsonResponse({ "message": "Created new follow" }, status=201)



@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def edit_post(request):

    # load the data
    data = json.loads(request.body)
  
    edited_post = {
        "user_id": request.user.pk,
        "text": data.get("text")
    }

    post = get_object_or_404(Posts, pk=data.get("post_id"))

    serializer = PostsSerializer(post, data=edited_post)

    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Post updated"}, status=200)


@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def like_post(request, post_id):

    # get the post to like/unlike
    post = get_object_or_404(Posts, pk=post_id)

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
            post.number_of_likes += 1
        else:
            post.number_of_likes -= 1
        
        post.save()

        return JsonResponse({ "message": "Updated liked status",
                                "like_count": post.number_of_likes}, status=200)
    
    # like doest exist 

    # increase like count on post on newly created like
    post.number_of_likes += 1
    post.save()

    
    # if user has never liked post before, create new record with default being liked (True)
    return JsonResponse({ "message": "Created new like",
                            "like_count": post.number_of_likes }, status=201)
        
    
