from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import django.utils.timezone


class MyUserManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')


        # if all inputs checkout, create the new user
        user = self.model(
            email=self.normalize_email(email), # converst characters lower case
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password) # =self._db ?
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    
    # need to implement for AbstractBaseUser
    username        = models.CharField(max_length=25, unique=True)
    date_joined	    = models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)
    last_login      = models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)
    is_admin        = models.BooleanField(default=False)
    is_active	    = models.BooleanField(default=True)
    is_staff	    = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)

    # used to specify what field to use to login
    USERNAME_FIELD = 'username'

    # filds reauired when user registering
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name',]

    # defining custom user manager
    objects = MyUserManager()

    def __str__(self):
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    
class Posts(models.Model):
    # 'related_name' is a reverse relationship i.e. user_posts = user has made all these posts 
    user_id   = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    text      = models.CharField(max_length=280)
    date_time = models.DateTimeField(default=django.utils.timezone.now)
    number_of_likes = models.IntegerField(default=0)


class Follows(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follows")
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed_by")
    is_following = models.BooleanField(default=True)


class Likes(models.Model):
    user_id  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_user_likes")
    post_id  = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="all_post_likes")
    is_liked  = models.BooleanField(default=True)
