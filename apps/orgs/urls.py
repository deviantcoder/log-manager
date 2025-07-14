from django.urls import path
from . import views

app_name = 'orgs'

urlpatterns = [
    path('create/', views.create_org, name='create_org'),
    path('settings/<str:id>/', views.org_settings, name='org_settings'),
    path('delete/<str:id>/', views.delete_org, name='delete_org'),
    path('delete/<str:id>/confirm/', views.delete_org_confirm, name='delete_org_confirm'),
    path('change-status/<str:id>/', views.change_org_status, name='change_org_status'),
    path('overview/<str:id>/', views.org_overview, name='org_overview'),
]