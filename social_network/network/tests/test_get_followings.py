import json
from django.test import TestCase
from rest_framework.test import APIClient
from network.models import User, Follows


class Tests(TestCase):

    def setUp(self):

        self.INVALID_ID = 99

        self.client = APIClient()

        # test users
        self.user1 = User.objects.create_user(username='test-user1', password="secret")
        self.user2 = User.objects.create_user(username='test-user2')
        self.user3 = User.objects.create_user(username='test-user3')
        self.user4 = User.objects.create_user(username='test-user4')

        self.client.login(username='test-user1', password='secret')


        # test follows (user 1 follows user 2, 3, and 4)
        Follows.objects.create(user_id=self.user1, user_following=self.user2)
        Follows.objects.create(user_id=self.user1, user_following=self.user3)
        Follows.objects.create(user_id=self.user1, user_following=self.user4)


    def test_get_user_following_count(self):

        # get followers cound for user1
        response = self.client.get(f"/api/user_following/{self.user1.pk}")

        # check response 200 ok
        self.assertEqual(response.status_code, 200)

        # JSON to py dict
        resp_dict = json.loads(response.content)

        # assert user 1 follows 3 users
        self.assertEqual(len(resp_dict), 3)
        

    def test_get_user_followers_count_error(self):

        # get followers count for user3
        response = self.client.get(f"/api/user_following/{self.INVALID_ID}")

        # check response 404 not found
        self.assertEqual(response.status_code, 404)

        # make invalid post request
        response = self.client.post(f"/api/user_following/{self.user3.pk}")

        # check invalid method not allowed request
        self.assertEqual(response.status_code, 405)
        