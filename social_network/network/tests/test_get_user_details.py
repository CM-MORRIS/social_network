import json
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import force_authenticate



from django.test import Client, TestCase, RequestFactory
from network.models import User
from network.views import user


class Tests(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(first_name="test", last_name="test", email="test1@email.com", password="secret", username='test-user1')
        self.user1 = User.objects.create_user(first_name="test", last_name="test", email="test2@email.com", password="secret", username='test-user2')

        self.request = self.factory.get(f"/api-auth/user/")
        force_authenticate(self.request, user=self.user)



    def test_get_user(self):

        response = user(self.request, self.user1.username)

        # check response 200 ok
        self.assertEqual(response.status_code, 200)

        # convert JSON response to python dict
        response_dict = json.loads(response.content)

        # retrieve 'username' from dict
        username = response_dict['username']

        # assert username returned from response is same as our created test user
        self.assertEqual(username, self.user1.username)
