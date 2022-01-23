import imp
from django.urls import path

from .views import FeedView

urlpatterns = [
    path('feed', FeedView.as_view(), name="feed"),
    path('feed/<article_id>', FeedView.as_view(), name="get_article"),
]
