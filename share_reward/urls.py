from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('content_ops/', include('content_ops.urls')),
    path('user_activity/', include('user_activity.urls'))
]
