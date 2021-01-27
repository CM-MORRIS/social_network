from django.contrib import admin
from .models import User, Posts, Follows, Likes

# Register your models here.
# admin user interface can be used to view, add, edit, delete from tables
# Use 'python manage.py createsuperuser' to create a superuser logged_in_user
# access admin page using '/admin'
# Register your models here.

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Follows)
admin.site.register(Likes)
