from .models import User, Posts, Follows, Likes
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(style={'input_type' : 'password'}, write_only=True, required=True)
    confirm_password = serializers.CharField(style={'input_type' : 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'confirm_password']

        # read only for security
        extra_kwargs = {
            'password': { 'write_only': True }
        }

    # if call .save in views this will get called
    def save(self):

        user = User (
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )

        password=self.validated_data['password']
        confirm_password=self.validated_data['confirm_password']

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'passwords must match'})

        user.set_password(password)
        user.save()
        
        return user


class UserSerializer(serializers.ModelSerializer):

    # the classes' class that creates the class
    # UserSerializer is a class but is actually an object !?
    # this Meta class actually creates the UserSerializer object 
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']


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


