import json
from django.test import Client, TestCase
from network.models import User


class Tests(TestCase):

    def setUp(self):

        self.client = Client()

        # test user to get
        self.user1 = User.objects.create_user(username='test-user1')


    def test_get_user(self):

        # specify user to get data for 
        response = self.client.get("/get_user/" + str(self.user1.pk))

        # check response 200 ok
        self.assertEqual(response.status_code, 200)

        # convert JSON response to python dict
        response_dict = json.loads(response.content)

        # retrieve 'username' from dict
        username = response_dict['username']

        # assert username returned from response is same as our created test user
        self.assertEqual(username, self.user1.username)


    def test_get_user_error(self):

        # specify user to get data for 
        response = self.client.post("/get_user/" + str(self.user1.pk))

        self.assertEqual(response.status_code, 400)
