from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('settings/', views.settings_view, name='settings'),
    path('inbox/', views.inbox, name='inbox'),
]