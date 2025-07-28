from django.urls import path
from apps.logs.views import api_views


app_name = 'api_logs'


urlpatterns = [
    path('logs/', api_views.LogIngestionAPIView.as_view(), name='log-ingestion'),
]
