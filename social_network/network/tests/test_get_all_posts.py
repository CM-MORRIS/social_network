import json
from django.test import Client, TestCase
from network.models import User, Posts


class Tests(TestCase):

    def setUp(self):

        self.client = Client()


        # test users to create the test posts
        user1 = User.objects.create_user(username='test-user1')
        user2 = User.objects.create_user(username='test-user2')

        # add multiple random posts from different users
        Posts.objects.create(user_id=user1, text="Test post")
        Posts.objects.create(user_id=user2, text="Test post")
        Posts.objects.create(user_id=user1, text="Test post")
        Posts.objects.create(user_id=user2, text="Test post")


# All Posts: The “All Posts” link in the navigation bar should take the user to a
# page where they can see all posts from all users, with the most recent posts first.

    def test_get_all_posts(self):

        # assert correct number is returned
        response = self.client.get("/all_posts")

        json_dict = json.loads(response.content)

        self.assertEqual(len(json_dict), 4)
    
    def test_get_all_posts_bad_request(self):

        # cannot make a POST request to this endpoint
        response = self.client.post("/all_posts")

        self.assertEqual(response.status_code, 400)
