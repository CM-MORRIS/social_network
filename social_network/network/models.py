from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone



class User(AbstractUser):
    # followers_count = models.IntegerField()
    # following_count = models.IntegerField()
    pass

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

    def serialize(self):
        return {
            "user_id": self.user_id.id,
            "text": self.text,
            "date_time": self.date_time.strftime("%b %-d %Y, %-I:%M %p"),
            "number_of_likes": self.number_of_likes
        }

class Follows(models.Model):
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follows")
    user_following  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed_by")
    isFollowing     = models.BooleanField(default=True)

class Likes(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_user_likes")
    post_id  = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="all_post_likes")
    isLiked  = models.BooleanField(default=True)
