from django.urls import path
from . import views


app_name = 'logs'


urlpatterns = [
    path('logs/', views.LogIngestionAPIView.as_view(), name='log-ingestion'),
]
