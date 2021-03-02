import json
from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate, APIRequestFactory

from network.models import User, Follows
from network.views import user_following


class Tests(TestCase):

    def setUp(self):

        self.INVALID_ID = 99

        self.client = APIClient()
        self.factory = APIRequestFactory()

        # test users
        self.user1 = User.objects.create_user(first_name="test", last_name="test", email="test1@email.com", username='test-user1', password="secret")
        self.user2 = User.objects.create_user(first_name="test", last_name="test", email="test2@email.com", username='test-user2', password="secret")
        self.user3 = User.objects.create_user(first_name="test", last_name="test", email="test3@email.com", username='test-user3', password="secret")
        self.user4 = User.objects.create_user(first_name="test", last_name="test", email="test4@email.com", username='test-user4', password="secret")
        self.user5 = User.objects.create_user(first_name="test", last_name="test", email="test5@email.com", username='test-user5', password="secret")

        self.client.login(username='test-user1', password='secret')

        # test follows (user 1 follows user 2, 3, and 4)
        Follows.objects.create(user_id=self.user1, user_following=self.user2)
        Follows.objects.create(user_id=self.user1, user_following=self.user3)
        Follows.objects.create(user_id=self.user1, user_following=self.user4)

        self.request = self.factory.get(f"/api-auth/user_following/")
        force_authenticate(self.request, user=self.user1)


    def test_get_user_following_count(self):

        response = user_following(self.request, self.user1.username)

        # check response 200 ok
        self.assertEqual(response.status_code, 200)

        # JSON to py dict
        resp_dict = json.loads(response.content)

        # assert user 1 follows 3 users
        self.assertEqual(resp_dict['followingCount'], 3)


    def test_get_user_followers_count_zero(self):

        # get followers count for user3
        response = user_following(self.request, self.user5)

         # check response 200 ok
        self.assertEqual(response.status_code, 200)

        # JSON to py dict
        resp_dict = json.loads(response.content)

        # assert user 1 follows 3 users
        self.assertEqual(resp_dict['followingCount'], 0)
    

    def test_get_user_followers_count_error(self):

        # get followers count for user3
        response = user_following(self.request, self.INVALID_ID)

        # check response 404 not found
        self.assertEqual(response.status_code, 404)

        