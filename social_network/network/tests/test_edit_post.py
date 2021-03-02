from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from network.models import User, Posts
from network.views import edit_post

# Create your tests here.
class Tests(TestCase):

    def setUp(self):

        # test users
        self.user1 = User.objects.create_user(first_name="test", last_name="test", email="test1@email.com", password="secret", username='test-user1')
        self.user2 = User.objects.create_user(first_name="test", last_name="test", email="test2@email.com", password="secret", username='test-user2')

        # test post for user1
        Posts.objects.create(pk=1, user_id=self.user1, text="Test post user1")

        # Every test needs access to the request factory.
        # Session and authentication attributes must be supplied
        # by the test itself if required for the view to function properly.
        self.factory = APIRequestFactory()
        self.client = APIClient()


    def test_edit_post(self):

        request_data = { 'text': 'Edit post text','post_id': 1 }

        # Create an instance of a PUT request.
        request = self.factory.put(
            '/api/edit_post', request_data, format='json')

        # simulate log in of user1
        force_authenticate(request, user=self.user1)

         # Test edit_post/ parsing in request
        response = edit_post(request)

        # assert 200 ok response
        self.assertEqual(response.status_code, 200)

        # asert post has been updated successfully
        test_post = Posts.objects.get(pk=1, user_id=self.user1)
        self.assertEqual(test_post.text, request_data["text"])
