import unittest
import json
from django.test import Client, TestCase, RequestFactory
from network.models import User, Posts
import django.utils.timezone
from rest_framework.test import APIRequestFactory, RequestsClient, APIClient
from rest_framework.test import force_authenticate

from network.views import create_post


# Create your tests here.
class Tests(TestCase):

    def setUp(self):

        # Every test needs access to the request factory.
        # Session and authentication attributes must be supplied
        # by the test itself if required for the view to function properly.
        self.factory = RequestFactory()

        self.user = User.objects.create_user(
            username='test-user', email='test@mail.com', password='secret')

    # test that when a POST is made to 'create_post' view
    # that a post is created by logged in user

    def test_create_post(self):

        data = {
            'text': 'This is a post'
        }

        # Create an instance of a GET request.
        request = self.factory.post(
            '/create_post', data, content_type='application/json')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test create_post() as if it were deployed at /create_post
        response = create_post(request)

        # 204 ok response
        self.assertEqual(response.status_code, 204)

        # check a new post has been added to table for user
        self.assertEqual(self.user.user_posts.count(), 1)

        # test the newly created post matches test post data
        post = Posts.objects.get(user_id=self.user)
        self.assertEqual(post.text, data.get("text"))


# 'context' is what is parsed to template when rendering html, i.e. the variable parsed through
# self.assertEqual(response.context["passengers"].count(), 1)

# RequestFactory returns a request, while Client returns a response.

# self.assertRedirects(response, '/catalog/')
