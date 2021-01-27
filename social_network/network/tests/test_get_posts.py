import json
from django.test import TestCase
from rest_framework.test import APIClient
from network.models import User, Posts
from django.db.models import Max

# These tests will test getting all posts that exist and getting specific user posts

class Tests(TestCase):

    def setUp(self):

        self.INVALID_USER_STRING = "This is invalid!"

        self.client = APIClient()

        # test users to create the test posts
        self.user1 = User.objects.create_user(username='test-user1', password="secret")
        self.user2 = User.objects.create_user(username='test-user2')
        self.user3 = User.objects.create_user(username='test-user3')

        # log in user1 just to bypass 'must be logged in' permission
        self.client.login(username='test-user1', password='secret')

        # get the max id for users
        self.MAX_ID = User.objects.all().aggregate(Max('id'))["id__max"]

        # add multiple random posts from different users
        Posts.objects.create(user_id=self.user1, text="Test post user1")
        Posts.objects.create(user_id=self.user2, text="Test post user2")
        Posts.objects.create(user_id=self.user1, text="Test post user1, no.2")
        Posts.objects.create(user_id=self.user2, text="Test post user 2, no.2")


    def test_get_all_posts(self):

        # assert correct number is returned
        response = self.client.get("/api/all_posts")

        # load response to python dict
        json_dict = json.loads(response.content)

        # assert response is as expected
        self.assertEqual(response.status_code, 200)

        # are all posts returned
        self.assertEqual(len(json_dict), 4)
    

    # getting user posts when they exist
    def test_get_user_posts(self):

        # request to get all posts for user1
        response = self.client.get(f"/api/user_posts/{self.user1.pk}")

        # load response to python dict
        json_dict = json.loads(response.content)

        # assert response is as expected
        self.assertEqual(response.status_code, 200)

        # are all posts returned
        self.assertEqual(len(json_dict), 2)
