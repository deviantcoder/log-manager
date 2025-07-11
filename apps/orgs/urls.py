from django.urls import path
from . import views

app_name = 'orgs'

urlpatterns = [
    path('create/', views.create_org, name='create_org'),
    path('settings/<str:id>/', views.org_settings, name='org_settings'),
]