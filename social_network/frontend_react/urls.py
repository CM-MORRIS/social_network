from django.urls import path, re_path
from frontend_react.views import *


urlpatterns = [
    path('', index),  # for the empty url
    re_path(r'^.*/$', index)  # for all other urls
]
