from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('accounts/social/', include('social_django.urls', namespace='social')),
    path('', include('apps.orgs.urls'))
]
