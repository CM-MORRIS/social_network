from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone

class User(AbstractUser):

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "email": self.email
        }

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

    def serialize(self):
        return {
            "user_id": self.user_id.id,
            "text": self.text,
            "date_time": self.date_time.strftime("%b %-d %Y, %-I:%M %p"),
            "number_of_likes": self.number_of_likes
        }

    def like(self):
        self.number_of_likes += 1
        self.save()
    
    def unlike(self):
        self.number_of_likes -= 1
        self.save()

class Follows(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follows")
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, 
                                             related_name="user_followed_by")
    is_following = models.BooleanField(default=True)

    def serialize(self):
        return {
            "user_id": self.user_id.username,
            "user_following": self.user_following.username,
            "is_following": self.is_following
        }


class Likes(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_user_likes")
    post_id  = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="all_post_likes")
    is_liked  = models.BooleanField(default=True)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "post_id": self.post_id,
            "isLiked": self.is_liked
        }
