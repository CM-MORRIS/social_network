import json
from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory, APIClient

from network.views import user_followers


from network.models import User, Follows


class Tests(TestCase):

    def setUp(self):

        self.INVALID_USER = 99

        self.client = APIClient()
        self.factory = APIRequestFactory()

        # test users
        self.user1 = User.objects.create_user(first_name="test", last_name="test", email="test1@email.com", password="secret", username='test-user1')
        self.user2 = User.objects.create_user(first_name="test", last_name="test", email="test2@email.com", password="secret", username='test-user2')
        self.user3 = User.objects.create_user(first_name="test", last_name="test", email="test3@email.com", password="secret", username='test-user3')
        self.user4 = User.objects.create_user(first_name="test", last_name="test", email="test4@email.com", password="secret", username='test-user4')
        self.user5 = User.objects.create_user(first_name="test", last_name="test", email="test5@email.com", password="secret", username='test-user5')


        self.user = User.objects.get(username='test-user1')
        
        
        # test follows (users 1, 2, 4, 5 follow user3)
        Follows.objects.create(user_id=self.user1, user_following=self.user3)
        Follows.objects.create(user_id=self.user2, user_following=self.user3)
        Follows.objects.create(user_id=self.user4, user_following=self.user3)
        Follows.objects.create(user_id=self.user5, user_following=self.user3)

        self.request = self.factory.get("/api-auth/user_followers/")
        force_authenticate(self.request, user=self.user)


    def test_user_followers_count(self):

        response = user_followers(self.request, self.user3.username)
      
        # check response 200 ok
        self.assertEqual(response.status_code, 200)

        # JSON to py dict
        resp_dict = json.loads(response.content)

        # assert there are 4 followers for user3
        self.assertEqual(resp_dict['followersCount'], 4)
        

    def test_user_followers_user_not_found(self):
       
        response = user_followers(self.request, self.INVALID_USER)

        # check response 404 not found
        self.assertEqual(response.status_code, 404)

        