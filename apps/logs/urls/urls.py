from django.urls import path
from apps.logs.views import views


app_name = 'logs'


urlpatterns = [
    path('projects/<str:project_id>/sources/create/', views.create_log_source, name='create_log_source'),

    path('sources/<str:source_id>/delete/', views.delete_log_source, name='delete_log_source'),
    path('sources/<str:source_id>/delete/confirm/', views.delete_log_source_confirm, name='delete_log_source_confirm'),

    path('sources/<str:source_id>/overview/', views.log_source_overview, name='log_source_overview'),
]
