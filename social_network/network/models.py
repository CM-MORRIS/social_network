from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone

class User(AbstractUser):
    pass

# to add extra fields to user do it with profile using onetoone for user
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     middle_name = models.CharField(max_length=30, blank=True)
#     dob = models.DateField(null=True, blank=True)


class Posts(models.Model):
    # 'related_name' is a reverse relationship i.e. user_posts = user has made all these posts 
    user_id   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    text      = models.CharField(max_length=280)
    date_time = models.DateTimeField(default=django.utils.timezone.now)
    number_of_likes = models.IntegerField(default=0)


class Follows(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follows")
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, 
                                             related_name="user_followed_by")
    is_following = models.BooleanField(default=True)


class Likes(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_user_likes")
    post_id  = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="all_post_likes")
    is_liked  = models.BooleanField(default=True)
