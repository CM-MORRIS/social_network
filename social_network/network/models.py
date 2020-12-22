from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone



class User(AbstractUser):
    # followers_count = models.IntegerField()
    # following_count = models.IntegerField()
    pass

class Posts(models.Model):
    # 'related_name' is a reverse relationship i.e. user_posts = user has made all these posts 
    user_id   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    text      = models.CharField(max_length=280)
    date_time = models.DateTimeField(default=django.utils.timezone.now)

class Follows(models.Model):
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follows")
    user_following  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed_by")
    isFollowing     = models.BooleanField(default=True)

class Likes(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_user_likes")
    post_id  = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="all_post_likes")
    isLiked  = models.BooleanField(default=True)
