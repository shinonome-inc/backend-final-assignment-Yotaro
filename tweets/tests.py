from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Tweet

User = get_user_model()


class TestHomeView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:home")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")

        self.tweet = Tweet.objects.create(user=self.user, content="this is a tweet")

    def test_success_get(self):
        response = self.client.get(self.url)
        tweets_db = Tweet.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/home.html")
        self.assertQuerysetEqual(response.context["tweets"], tweets_db)


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.url = reverse("tweets:create")
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="this is a tweet")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        valid_data = {"content": "tweet"}
        response = self.client.post(self.url, valid_data)

        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
        )
        self.assertTrue(Tweet.objects.filter(content=valid_data["content"]).exists())

    def test_failure_post_with_empty_content(self):
        invalid_data = {"content": ""}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(content=invalid_data["content"]).exists())
        self.assertIn("このフィールドは必須です。", form.errors["content"])

    def test_failure_post_with_too_long_content(self):
        invalid_data = {"content": "a" * 290}
        response = self.client.post(self.url, invalid_data)
        form = response.context["form"]

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(content=invalid_data["content"]).exists())
        self.assertIn(f"この値は 280 文字以下でなければなりません( {len(invalid_data['content'])} 文字になっています)。", form.errors["content"])


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="this is a tweet")
        self.url = reverse("tweets:detail", kwargs={"pk": self.tweet.pk})

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["tweet"], self.tweet)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.another_user = User.objects.create_user(username="another_testuser", password="another_password")
        self.client.login(username="testuser", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="this is a tweet")
        self.another_tweet = Tweet.objects.create(user=self.another_user, content="this is another tweet")
        self.url = reverse("tweets:delete", kwargs={"pk": self.tweet.pk})
        self.another_url = reverse("tweets:delete", kwargs={"pk": self.another_tweet.pk})
        self.non_existent_url = reverse("tweets:delete", kwargs={"pk": 9999})

    def test_success_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("tweets:home"), status_code=302)
        self.assertFalse(Tweet.objects.filter(pk=self.tweet.pk).exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(self.non_existent_url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Tweet.objects.filter(pk=self.tweet.pk).exists())

    def test_failure_post_with_incorrect_user(self):
        response = self.client.post(self.another_url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Tweet.objects.filter(pk=self.another_tweet.pk).exists())


# class TestLikeView(TestCase):
#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_liked_tweet(self):


# class TestUnLikeView(TestCase):

#     def test_success_post(self):

#     def test_failure_post_with_not_exist_tweet(self):

#     def test_failure_post_with_unliked_tweet(self):
