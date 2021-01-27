import json
from django.test import TestCase
from rest_framework.test import APIClient

from network.models import User, Follows


class Tests(TestCase):

    def setUp(self):

        self.INVALID_USER = 99

        self.client = APIClient()

        # test users
        self.user1 = User.objects.create_user(username='test-user1', password="secret")
        self.user2 = User.objects.create_user(username='test-user2')
        self.user3 = User.objects.create_user(username='test-user3')
        self.user4 = User.objects.create_user(username='test-user4')
        self.user5 = User.objects.create_user(username='test-user5')

        # log in user1 just to bypass 'must be logged in' permission
        self.client.login(username='test-user1', password='secret')

        # test follows (users 1, 2, 4, 5 follow user3)
        Follows.objects.create(user_id=self.user1, user_following=self.user3)
        Follows.objects.create(user_id=self.user2, user_following=self.user3)
        Follows.objects.create(user_id=self.user4, user_following=self.user3)
        Follows.objects.create(user_id=self.user5, user_following=self.user3)


    def test_user_followers_count(self):

        # get followers for user3
        response = self.client.get(f"/api/user_followers/{self.user3.pk}")

        # check response 200 ok
        self.assertEqual(response.status_code, 200)

        # JSON to py dict
        resp_dict = json.loads(response.content)

        # assert there are 4 followers for user3
        self.assertEqual(len(resp_dict), 4)
        

    def test_user_followers_user_not_found(self):

        # get followers cound for user3
        response = self.client.get(f"/api/user_followers/{self.INVALID_USER}")

        # check response 404 not found
        self.assertEqual(response.status_code, 404)

        