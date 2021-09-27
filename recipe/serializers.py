from rest_framework import serializers

from core.models import Tag, Article


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer for article objects"""

    class Meta:
        model = Article
        fields = ('id', 'summarize')
        read_only_fields = ('id',)
