from django.test import Client, TestCase, RequestFactory
from network.models import User, Posts
from network.views import create_post


# Create your tests here.
class Tests(TestCase):

    def setUp(self):

        # Every test needs access to the request factory.
        # Session and authentication attributes must be supplied
        # by the test itself if required for the view to function properly.
        self.factory = RequestFactory()
        self.client = Client()

        self.user = User.objects.create_user(
            username='test-user', email='test@mail.com', password='secret')

        self.data = {'text': 'This is a post'}

    # test that when a POST is made to 'create_post' view
    # that a post is created by logged in user

    def test_create_post(self):

        # Create an instance of a POST request.
        request = self.factory.post(
            '/create_post', self.data, content_type='application/json')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test create_post() as if it were deployed at /create_post
        response = create_post(request)

        # 204 ok response
        self.assertEqual(response.status_code, 204)

        # check a new post has been added to table for user
        self.assertEqual(self.user.user_posts.count(), 1)

        # test the newly created post matches test post data
        post = Posts.objects.get(user_id=self.user)
        self.assertEqual(post.text, self.data.get("text"))

    def test_create_post_bad_request(self):

        # Create an instance of a GET request.
        request = self.factory.get(
            '/create_post', self.data, content_type='application/json')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test create_post() as if it were deployed at /create_post
        response = create_post(request)

        # bad request
        self.assertEqual(response.status_code, 400)

    def test_create_post_not_logged_in(self):

        # no user logged in when making this request
        response = self.client.post("/create_post",
                                    self.data, content_type='application/json')

        # '@login_required' in views redirects to the
        # login page if the user is not logged in so returns 302
        self.assertEqual(response.status_code, 302)
