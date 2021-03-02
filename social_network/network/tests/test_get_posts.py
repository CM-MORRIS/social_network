import json
from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory, APIClient
from network.models import User, Posts
from django.db.models import Max

from network.views import all_posts, user_posts


# These tests will test getting all posts that exist and getting specific user posts

class Tests(TestCase):

    def setUp(self):

        self.INVALID_USER_STRING = "This is invalid!"

        self.client = APIClient()
        self.factory = APIRequestFactory()

        # test users to create the test posts
        self.user1 = User.objects.create_user(first_name="test", last_name="test", email="test1@email.com", password="secret", username='test-user1')
        self.user2 = User.objects.create_user(first_name="test", last_name="test", email="test2@email.com", password="secret", username='test-user2')
        self.user3 = User.objects.create_user(first_name="test", last_name="test", email="test3@email.com", password="secret", username='test-user3')
        
        # get the max id for users
        self.MAX_ID = User.objects.all().aggregate(Max('id'))["id__max"]

        # add multiple random posts from different users
        Posts.objects.create(user_id=self.user1, text="Test post user1")
        Posts.objects.create(user_id=self.user2, text="Test post user2")
        Posts.objects.create(user_id=self.user1, text="Test post user1, no.2")
        Posts.objects.create(user_id=self.user2, text="Test post user 2, no.2")


    
    def test_get_all_posts(self):

        request = self.factory.get("/api-auth/all_posts/")
        force_authenticate(request, user=self.user1)

        # get all posts
        response = all_posts(request)

        # check response 200 ok
        self.assertEqual(response.status_code, 200)

        # load response to python dict
        res_dict = json.loads(response.content)

        # are all posts returned
        self.assertEqual(len(res_dict), 4)
    

    # getting user posts when they exist
    def test_get_user_posts(self):

        # request to get all posts for user1
        request = self.factory.get("/api-auth/user_posts")
        force_authenticate(request, user=self.user1)

        # get all posts
        response = user_posts(request, self.user1.pk)

        # load response to python dict
        json_dict = json.loads(response.content)

        # assert response is as expected
        self.assertEqual(response.status_code, 200)

        # are all posts returned
        self.assertEqual(len(json_dict), 2)
