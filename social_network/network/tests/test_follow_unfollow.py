from django.test import Client, TestCase, RequestFactory
from network.models import User, Follows
from network.views import follow

class Tests(TestCase):

    def setUp(self):

        self.INVALID_USERNAME = "This is an invalid username!"

        self.client = Client()
        self.factory = RequestFactory()

        # test users
        self.user1 = User.objects.create_user(username='test-user1')
        self.user2 = User.objects.create_user(username='test-user2')
        self.user3 = User.objects.create_user(username='test-user3')
        self.user4 = User.objects.create_user(username='test-user4')

        # Create an instance of a POST request.
        self.request = self.factory.post(f"/follow/{self.user1.username}")

        # Simulate logged-in user by setting request.user manually.
        # log in user4
        self.request.user = self.user4

         # post request to follow - user4 will follow user1
        response = follow(self.request, self.user1.username)

        # has content been created
        self.assertEqual(response.status_code, 201)


    def test_new_follow(self):

        # is user4 following user1 automatically set to True on creation
        test_follow_true = Follows.objects.get(user_id=self.user4, user_following=self.user1)
        self.assertTrue(test_follow_true.isFollowing)

    
    def test_unfollow(self):

        # post request to follow - user4 will unfollow user1
        response = follow(self.request, self.user1.username)
        self.assertEqual(response.status_code, 200)

        # is user4 following user1 set to False for unfollow
        test_follow_false = Follows.objects.get(user_id=self.user4, user_following=self.user1)
        self.assertFalse(test_follow_false.isFollowing)

        
    def test_refollow(self):

        # initial request to create a follow
        response = follow(self.request, self.user2.username)
        self.assertEqual(response.status_code, 201)
        obj = Follows.objects.get(user_id=self.user4, user_following=self.user2)
        self.assertTrue(obj.isFollowing)

        # make second request to unfollow
        response = follow(self.request, self.user2.username)
        self.assertEqual(response.status_code, 200)
        obj = Follows.objects.get(user_id=self.user4, user_following=self.user2)
        self.assertFalse(obj.isFollowing)

        # make third request to refollow
        response = follow(self.request, self.user2.username)
        self.assertEqual(response.status_code, 200)
        obj = Follows.objects.get(user_id=self.user4, user_following=self.user2)
        self.assertTrue(obj.isFollowing)
    

    def test_follow_request_invalid_user(self):

        # make request with invalid username
        response = follow(self.request, self.INVALID_USERNAME)
        self.assertEqual(response.status_code, 404)
    

    def test_follow_invalid_request(self):

        # make request with invalid username
        response = follow(self.request, self.INVALID_USERNAME)
        self.assertEqual(response.status_code, 404)


    def test_follow_self(self):

        # make request user follow self
        response = follow(self.request, self.user4.username)
        self.assertEqual(response.status_code, 404)


