import json
from rest_framework.permissions import IsAuthenticated, AllowAny
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
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Posts, Follows, Likes
from .serializers import PostsSerializer, UserSerializer, FollowsSerializer, LikesSerializer, RegistrationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def logoutAndBlacklistRefreshTokenForUser(request):

    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)

    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def helloWorldView(request):

    return JsonResponse({"hello":"hello, world"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
 
    serializer = RegistrationSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return JsonResponse({"message":"Successfully registered user"}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request, username):

    user = User.objects.get(username=username)
    serializer = UserSerializer(user, many=False)

    return JsonResponse(serializer.data, status=200)

@api_view(['GET'])
@permission_classes([AllowAny])
def user_exists(request, username):

    if (User.objects.filter(username=username).exists()):
        return JsonResponse({"exists": True}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"exists": False}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def email_exists(request, email):

    if (User.objects.filter(email=email).exists()):
        return JsonResponse({"exists": True}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({"exists": False}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_logged_in_user(request):

    user_logged_in = request.user.username

    return JsonResponse({"user_logged_in": user_logged_in}, status=200)


@api_view(['GET'])
@permission_classes([AllowAny])
def is_user_logged_in(request):

    is_user_logged_in = request.user.is_authenticated

    return JsonResponse({"is_user_logged_in": is_user_logged_in}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_posts(request):

    # get all posts ordered by date ascending
    all_posts = Posts.objects.order_by("-date_time").all()
    serializer = PostsSerializer(all_posts, many=True)

    return JsonResponse(serializer.data, status=200, safe=False)


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_posts(request, username):

    user = get_object_or_404(User, username=username)
    user_posts = user.user_posts
    user_posts = user_posts.order_by("-date_time")

    serializer = PostsSerializer(user_posts, many=True)

    return JsonResponse(serializer.data, status=200, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_followers(request, username):

    user = get_object_or_404(User, username=username)
    followers = user.user_followed_by

    followers_count = followers.count()

    serializer = FollowsSerializer(followers, many=True)


    return JsonResponse(data={"followersList":serializer.data, "followersCount": followers_count}, status=200, safe=False)
    #return JsonResponse(data={"followers": str(followers)}, status=200, safe=False)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_following(request, username):

    user = get_object_or_404(User, username=username)
    follows = user.user_follows

    following_count = follows.count()

    serializer = FollowsSerializer(follows, many=True)

    return JsonResponse(data={"followingList":serializer.data, "followingCount": following_count}, status=200, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_following(request, username):
    
    logged_in_user = request.user.pk

    user_profile = get_object_or_404(User, username=username)

    user_profile = Follows.objects.filter(
        user_id=logged_in_user, user_following=user_profile, is_following=True).exists()

    if user_profile is True:
        return JsonResponse({"isFollowing": True}, status=200, safe=False)
    else:
        return JsonResponse({"isFollowing": False}, status=200, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    
    user_to_follow = get_object_or_404(User, username=username)

    if (request.user.username == username):
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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
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
        
    
