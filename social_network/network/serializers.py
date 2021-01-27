from .models import User, Posts, Follows, Likes
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    # the classes' class that creates the class
    # UserSerializer is a class but is actually an object !?
    # this Meta class actually creates the UserSerializer object 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']


class PostsSerializer(serializers.ModelSerializer):

    # read_only=True to ensure that the field is used when serializing a representation, 
    # but is not used when creating or updating an instance during deserialization.
    username = serializers.CharField(source='user_id.username', read_only=True)

    class Meta:
        model = Posts
        fields = ['pk', 'user_id', 'username', 'text', 'date_time', 'number_of_likes']


class FollowsSerializer(serializers.ModelSerializer):

    user = serializers.CharField(source='user_id.username', read_only=True)
    user_following = serializers.CharField(source='user_following.username', read_only=True)

    class Meta:
        model = Follows
        fields = ['user', 'user_following', 'is_following']


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'


