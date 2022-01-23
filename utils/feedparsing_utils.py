import datetime
from unicodedata import category
import pytz

import feedparser
from random import sample, randint
from linkpreview import link_preview

from content_ops.models import ChannelRssData, ContentCategories, ArticleData, CronActivity


all_categories = list(
    ContentCategories.objects.all().values_list('id', flat=True))
print(all_categories)


def get_url_info_dict(url, date):
    preview = link_preview(url)
    return {"title": preview.title,
            "description": preview.description,
            "image": preview.image,
            'date_published': date_str}


channel_objs = ChannelRssData.objects.filter(is_active=True)
output = []
for channel_obj in channel_objs:
    feed_url = channel_obj.feed_url

    NewsFeed = feedparser.parse(feed_url)
    for entry in NewsFeed.entries:
        link = entry['link'].strip()
        date_str = entry.get('published', None)
        info = get_url_info_dict(link, date_str)
        info['channel'] = channel_obj

        article_obj, _ = ArticleData.objects.get_or_create(
            url=link, defaults=info)

        article_obj.categories.clear()

        categories = sample(all_categories, randint(1, 2))
        category_objs = ContentCategories.objects.filter(id__in=categories)
        for category_obj in category_objs:
            article_obj.categories.add(category_obj)
        article_obj.save()

        print(article_obj.id)

    crr_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    CronActivity.objects.update_or_create(
        channel=channel_obj, defaults={'last_croned': crr_time})
