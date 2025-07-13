from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create/', views.create_project, name='create_project'),
    path('settings/<str:id>/', views.project_settings, name='project_settings'),
    path('delete/<str:id>/', views.delete_project, name='delete_project'),
    path('delete/<str:id>/confirm/', views.delete_project_confirm, name='delete_project_confirm'),
    path('change-status/<str:id>/', views.change_project_status, name='change_project_status'),
]