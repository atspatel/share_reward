from django.contrib import admin
from django.apps import apps

# Register your models here
from .models import ContentCategories, ChannelRssData, CronActivity, ArticleData


class ContentCategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag']


admin.site.register(ContentCategories, ContentCategoriesAdmin)


class ChannelRssDataAdmin(admin.ModelAdmin):
    list_display = ["id", "channel_name", "feed_url", "is_active"]


admin.site.register(ChannelRssData, ChannelRssDataAdmin)


class CronActivityAdmin(admin.ModelAdmin):
    list_display = ['channel', "last_croned"]


admin.site.register(CronActivity, CronActivityAdmin)


class ArticleDataAdmin(admin.ModelAdmin):
    list_display = ["url", "title", "date_published"]


admin.site.register(ArticleData, ArticleDataAdmin)

app = apps.get_app_config('accounts')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except:
        continue
