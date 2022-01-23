from django.contrib import admin
from django.apps import apps

# Register your models here
from .models import UserLikeTable, ConnectionTable, UserShareTable, ConnectionRewardValue


class UserLikeTableAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'article', "creation_time"]


admin.site.register(UserLikeTable, UserLikeTableAdmin)


class ConnectionTableAdmin(admin.ModelAdmin):
    list_display = ["id", "user_a", "user_b"]


admin.site.register(ConnectionTable, ConnectionTableAdmin)


class UserShareTableAdmin(admin.ModelAdmin):
    list_display = ["connection", "article", 'reward_earned', 'status']


admin.site.register(UserShareTable, UserShareTableAdmin)


class ConnectionRewardValueAdmin(admin.ModelAdmin):
    list_display = ["connection", "category",
                    "article_shared", "article_opened"]


admin.site.register(ConnectionRewardValue, ConnectionRewardValueAdmin)

app = apps.get_app_config('accounts')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except:
        continue
