from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path, include
from django.views import generic

from django.conf import settings
from django.conf.urls.static import static

from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', generic.TemplateView.as_view(template_name="_base.html")),
    
    path('accounts/', include('apps.accounts.urls')),
    path('accounts/social/', include('social_django.urls', namespace='social')),
    
    path('dashboard/', include('apps.dashboard.urls')),
    path('dashboard/organizations/', include('apps.orgs.urls')),
    path('dashboard/', include('apps.projects.urls')),

    path('api/', include('apps.logs.urls')),
    path('api-auth/', include('rest_framework.urls')),

    # password reset
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(template_name='password_reset/reset_password.html'),
        name='reset_password'
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'),
        name='password_reset_complete'
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += debug_toolbar_urls()
