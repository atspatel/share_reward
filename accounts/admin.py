from django.contrib import admin
from django.apps import apps

# Register your models here
from .models import User, UserOTPTable


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'first_name',
                    'is_admin', 'is_verified', "creation_time"]


admin.site.register(User, UserAdmin)


class UserOTPTableAdmin(admin.ModelAdmin):
    list_display = ["phone", "otp", "creation_time"]


admin.site.register(UserOTPTable, UserOTPTableAdmin)

app = apps.get_app_config('accounts')
for model_name, model in app.models.items():
    try:
        admin.site.register(model)
    except:
        continue
