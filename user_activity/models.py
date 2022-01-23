from operator import mod
from statistics import mode
from unicodedata import category
from django.db import models
from accounts.models import AbstractTimeClass, User
from content_ops.models import ArticleData, ContentCategories


class UserLikeTable(AbstractTimeClass):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleData, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['user', 'article']


class ConnectionTable(AbstractTimeClass):
    user_a = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shared_by')
    user_b = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shared_with')
    REQUIRED_FIELDS = ['user_a', 'user_b']

    def __str__(self):
        return "%s <> %s" % (self.user_a.first_name, self.user_b.first_name)


class UserShareTable(AbstractTimeClass):
    connection = models.ForeignKey(ConnectionTable, on_delete=models.CASCADE, )
    article = models.ForeignKey(ArticleData, on_delete=models.CASCADE)
    reward_earned = models.FloatField(default=0.0)

    status = models.IntegerField(default=0)
    # 0 -> shared, 1 -> opened

    REQUIRED_FIELDS = ["connection", 'article']


class ConnectionRewardValue(AbstractTimeClass):
    connection = models.ForeignKey(ConnectionTable, on_delete=models.CASCADE)
    category = models.ForeignKey(ContentCategories, on_delete=models.CASCADE)
    article_shared = models.IntegerField(default=0)
    article_opened = models.IntegerField(default=0)
