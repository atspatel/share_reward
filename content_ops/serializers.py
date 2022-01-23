from rest_framework import serializers
from .models import ArticleData, ChannelRssData, ContentCategories


class ChannelRssDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelRssData
        fields = ('id', 'channel_name', 'channel_image')


class ContentCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentCategories
        fields = ('id', 'tag')


class ArticleDataSerializer(serializers.ModelSerializer):

    source = ChannelRssDataSerializer(source='channel', read_only=True)
    categories_list = ContentCategoriesSerializer(
        source='categories', many=True, read_only=True)

    class Meta:
        model = ArticleData
        fields = ('id', 'url', 'title', 'description',
                  'image', 'date_published', 'source', 'categories_list')
