import json
import requests
from django.test import Client, TestCase
from network.models import User, Posts


class Tests(TestCase):

    def setUp(self):

        self.client = Client()

        # test users to create the test posts
        self.user1 = User.objects.create_user(username='test-user1')


    def test_get_user(self):

        response = self.client.get("/get_user/" + str(self.user1.pk))

        # convert JSON response to python dict
        response_dict = json.loads(response.content)

        # retrieve 'username' from dict
        username = response_dict['username']

        # assert username returned from response is as expected
        self.assertEqual(username, self.user1.username)
    
    # def test_get_all_posts_bad_request(self):

    #     # cannot make a POST request to this endpoint
    #     response = self.client.post("/all_posts")

    #     self.assertEqual(response.status_code, 400)
