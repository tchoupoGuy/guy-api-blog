from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Article
from recipe.serializers import ArticleSerializer

ARTICLES_URL = reverse('recipe:article-list')


class PublicArticlesApiTests(TestCase):
    """Test the publicly available articles API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(ARTICLES_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateArticlesApiTest(TestCase):
    """test the private Articles API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@guy.com', 'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieving_articles_list(self):
        """Test retrieving a list of Article"""
        Article.objects.create(user=self.user, summarize='good article')
        Article.objects.create(user=self.user, summarize='like it')

        res = self.client.get(ARTICLES_URL)

        articles = Article.objects.all().order_by('-summarize')
        serializer = ArticleSerializer(articles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_articles_limited_to_user(self):
        """"Test that any articles for the authenticate user are return"""
        user2 = get_user_model().objects.create_user(
            'other@guy.com',
            'testpass'
        )
        Article.objects.create(user=user2, summarize='yes is good')
        article = Article.objects.create(user=self.user, summarize='good and favorite')

        res = self.client.get(ARTICLES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['summarize'], article.summarize)

    def test_create_article_successful(self):
        """test create a new article"""
        payload = {'summarize': 'yes this the article'}
        self.client.post(ARTICLES_URL, payload)

        exists = Article.objects.filter(
            user=self.user,
            summarize=payload['summarize'],
        ).exists()
        self.assertTrue(exists)

    def test_create_article_invalid(self):
        """Test creating invalid article fails"""
        payload = {'summarize': ''}
        res = self.client.post(ARTICLES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)