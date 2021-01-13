from django.test import Client, TestCase, RequestFactory
from network.models import User, Posts
from network.views import edit_post


# Create your tests here.
class Tests(TestCase):

    def setUp(self):

        # test users
        self.user1 = User.objects.create_user(username='test-user1')
        self.user2 = User.objects.create_user(username='test-user2')

        # test post for user1
        Posts.objects.create(pk=1, user_id=self.user1, text="Test post user1")

        # Every test needs access to the request factory.
        # Session and authentication attributes must be supplied
        # by the test itself if required for the view to function properly.
        self.factory = RequestFactory()
        self.client = Client()


    def test_edit_post(self):

        request_data = {'text': 'Edit post text','post_id': 1 }

        # Create an instance of a PUT request.
        request = self.factory.put(
            '/edit_post', request_data, content_type='application/json')

        # simulate log in of user1
        request.user = self.user1

         # Test edit_post/ parsing in request
        response = edit_post(request)

        # assert 200 ok response
        self.assertEqual(response.status_code, 200)

        # asert post has been updated successfully
        test_post = Posts.objects.get(pk=1, user_id=self.user1)
        self.assertEqual(test_post.text, request_data["text"])

    def test_edit_post_not_logged_in(self):

        request_data = {'text': 'Edit post text','post_id': 1}

        # Create an instance of a PUT request.
        response = self.client.put("/edit_post", request_data, content_type='application/json')

         # assert 404 response indicating user not logged in
        self.assertEqual(response.status_code, 302)

    def test_edit_post_bad_request(self):

        request_data = {'text': 'Edit post text','post_id': 1 }

        # Create an instance of invalid POST request.
        request = self.factory.post(
            '/edit_post', request_data, content_type='application/json')

        # simulate log in of any user1 don't actually need user for this test
        request.user = self.user1

         # Test edit_post/ parsing in request
        response = edit_post(request)

         # assert 400 response indicating bad request (request has to be PUT)
        self.assertEqual(response.status_code, 400)


    def test_edit_post_can_only_edit_own_posts(self):

        request_data = {'text': 'Edit post text','post_id': 1 }

        # Create an instance of invalid POST request.
        request = self.factory.put(
            '/edit_post', request_data, content_type='application/json')

        # simulate log in of user2 trying to edit user1 post
        request.user = self.user2

         # Test edit_post/ parsing in request
        response = edit_post(request)

         # assert 404 response indicating post to edit doesn't 
         # exist as it doesn't belong to logged in user
        self.assertEqual(response.status_code, 404)

