from django.test import TestCase
from rest_framework.test import force_authenticate, APIRequestFactory, APIClient
from network.models import User, Follows
from network.views import follow

class Tests(TestCase):

    def setUp(self):

        self.INVALID_USERID = 99

        self.client = APIClient()
        self.factory = APIRequestFactory()

        # test users
        self.user1 = User.objects.create_user(first_name="test", last_name="test", email="test1@email.com", password="secret", username='test-user1')
        self.user2 = User.objects.create_user(first_name="test", last_name="test", email="test2@email.com", password="secret", username='test-user2')
        self.user3 = User.objects.create_user(first_name="test", last_name="test", email="test3@email.com", password="secret", username='test-user3')
        self.user4 = User.objects.create_user(first_name="test", last_name="test", email="test4@email.com", password="secret", username='test-user4')

        # Create an instance of a POST request.
        self.request = self.factory.post(f"/api-auth/follow/")

        # Simulate logged-in user by setting request.user manually.
        # log in user4
        force_authenticate(self.request, user=self.user4)

         # post request to follow - user4 will follow user1
        response = follow(self.request, self.user1.username)

        # has content been created
        self.assertEqual(response.status_code, 201)


    def test_new_follow(self):

        # is user4 following user1 automatically set to True on creation
        test_follow_true = Follows.objects.get(user_id=self.user4, user_following=self.user1)
        self.assertTrue(test_follow_true.is_following)

    
    def test_unfollow(self):

        # post request to follow - user4 will unfollow user1
        response = follow(self.request, self.user1.username)
        self.assertEqual(response.status_code, 200)

        # is user4 following user1 set to False for unfollow
        test_follow_false = Follows.objects.get(user_id=self.user4, user_following=self.user1)
        self.assertFalse(test_follow_false.is_following)

        
    def test_refollow(self):

        # request to create a follow
        response = follow(self.request, self.user2.username)
        self.assertEqual(response.status_code, 201)
        obj = Follows.objects.get(user_id=self.user4, user_following=self.user2)
        self.assertTrue(obj.is_following)

        # make second request to unfollow
        response = follow(self.request, self.user2.username)
        self.assertEqual(response.status_code, 200)
        obj = Follows.objects.get(user_id=self.user4, user_following=self.user2)
        self.assertFalse(obj.is_following)

        # make third request to refollow
        response = follow(self.request, self.user2.username)
        self.assertEqual(response.status_code, 200)
        obj = Follows.objects.get(user_id=self.user4, user_following=self.user2)
        self.assertTrue(obj.is_following)
    

    def test_follow_request_invalid_user(self):

        # make request with invalid username
        response = follow(self.request, self.INVALID_USERID)
        self.assertEqual(response.status_code, 404)
    

    def test_follow_invalid_request(self):

        # make request with invalid username
        response = follow(self.request, self.INVALID_USERID)
        self.assertEqual(response.status_code, 404)


    def test_follow_self(self):

        # make request user follow self
        response = follow(self.request, self.user4.username)
        self.assertEqual(response.status_code, 404)


