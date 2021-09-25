from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

# from recipe.serializers import ArticleSerializer

ARTICLE_URL = reverse('recipe:article-list')

class PublicArticlesApiTests(TestCase):
    """Test the publicly available article API"""

    def setUp(self):
        self.client = APIClient
