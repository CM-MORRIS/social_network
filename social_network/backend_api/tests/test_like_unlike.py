from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from backend_api.models import User, Posts, Likes
from backend_api.views import like_post

class Tests(TestCase):

    def setUp(self):

        self.client = APIClient()
        self.factory = APIRequestFactory()

        # test users
        self.user1 = User.objects.create_user(first_name="test", last_name="test", email="test1@email.com", password="secret", username='test-user1')
        self.user2 = User.objects.create_user(first_name="test", last_name="test", email="test2@email.com", password="secret", username='test-user2')

        # test posts
        self.post1 = Posts.objects.create(pk=1, user_id=self.user2, text="Test post user1")

        # Simulate logged-in user1 by setting request.user manually.
        self.request = self.factory.put(f"/api-auth/like_post/{self.post1.pk}")
        force_authenticate(self.request, user=self.user1)


    def test_new_like(self):

        # put request to like_post - logged in user1 will like post1 
        response = like_post(self.request, self.post1.pk)

        # assert new like is created
        self.assertEqual(response.status_code, 201)

        # assert the newly created like - is_liked column - is True
        created_like = Likes.objects.get(user_id=self.user1, post_id=self.post1)
        self.assertTrue(created_like.is_liked)

    
    def test_unlike(self):

        # put request to like_post - logged in user1 will like post1 
        response = like_post(self.request, self.post1.pk)

        # assert new like is created
        self.assertEqual(response.status_code, 201)

        # put request to like_post - logged in user1 will unlike post1 
        response = like_post(self.request, self.post1.pk)

        # assert the like record was updated
        self.assertEqual(response.status_code, 200)

        # assert the is_liked column is False for unlike
        created_like = Likes.objects.get(user_id=self.user1, post_id=self.post1)
        self.assertFalse(created_like.is_liked)

    def test_like_count_increase(self):

        # assert post has zero likes before beginning tests
        self.assertEqual(self.post1.number_of_likes, 0)

        # user1 (already logged in in setUp) like post1
        response = like_post(self.request, self.post1.pk)
        self.assertEqual(response.status_code, 201)

        # log in user2
        force_authenticate(self.request, user=self.user2)

        # user2 like post1
        response = like_post(self.request, self.post1.pk)
        self.assertEqual(response.status_code, 201)

        # assert post now has 2 likes
        self.assertEqual(Posts.objects.get(pk=1).number_of_likes, 2)

         # user2 unlike post1
        response = like_post(self.request, self.post1.pk)
        self.assertEqual(response.status_code, 200)

        # assert post now has 1 like
        self.assertEqual(Posts.objects.get(pk=1).number_of_likes, 1)
