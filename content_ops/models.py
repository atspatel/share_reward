from unicodedata import category
from django.db import models
from accounts.models import AbstractTimeClass


class ContentCategories(AbstractTimeClass):
    tag = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.tag


class ChannelRssData(AbstractTimeClass):
    feed_url = models.URLField(unique=True, null=False, blank=False)
    channel_name = models.CharField(max_length=100)
    channel_image = models.URLField(null=True)

    is_active = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['feed_url', 'channel_name']

    def __str__(self):
        return self.channel_name


class CronActivity(AbstractTimeClass):
    channel = models.ForeignKey(ChannelRssData, on_delete=models.CASCADE)
    last_croned = models.DateTimeField(null=False, blank=False)


class ArticleData(AbstractTimeClass):
    url = models.URLField(unique=True, null=False, blank=False)
    title = models.TextField(blank=False, null=False)
    description = models.TextField()
    image = models.URLField()
    categories = models.ManyToManyField(ContentCategories, blank=True)
    date_published = models.CharField(max_length=100)
    channel = models.ForeignKey(
        ChannelRssData, on_delete=models.CASCADE, blank=True)

    REQUIRED_FIELDS = ['url', 'title']

    def __str__(self):
        return self.title
