from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from backend_api.models import User, Posts
from backend_api.views import create_post


# Create your tests here.
class Tests(TestCase):

    def setUp(self):

        # Every test needs access to the request factory.
        # Session and authentication attributes must be supplied
        # by the test itself if required for the view to function properly.
        self.factory = APIRequestFactory()
        self.client = APIClient()

        self.user = User.objects.create_user(
            first_name="test", last_name="test", username='test-user', email='test@mail.com', password='secret')

        self.data = {"text": "This is a post"}

        # Create an instance of a POST request.
        self.request = self.factory.post(
            '/api/create_post', self.data, format='json')

        force_authenticate(self.request, user=self.user)


    def test_create_post(self):

        # Test create_post() as if it were deployed at /create_post
        response = create_post(self.request)

        # response = self.client.post('/create_post', self.data, format='json')

        # 201 ok response
        self.assertEqual(response.status_code, 201)

        # # check a new post has been added to table for user
        # self.assertEqual(self.user.user_posts.count(), 1)

        # test the newly created post matches test post data
        post = Posts.objects.get(user_id=self.user)
        self.assertEqual(post.text, self.data.get("text"))


    def test_create_post_bad_request(self):

        invalid_data = {"not_valid": "not a valid request"}

        request = self.factory.post(
        '/api/create_post', invalid_data, format='json')

        force_authenticate(request, user=self.user)

        response = create_post(request)

        # bad request
        self.assertEqual(response.status_code, 400)
