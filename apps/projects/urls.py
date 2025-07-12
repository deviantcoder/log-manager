from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('create/', views.create_project, name='create_project'),
    path('settings/<str:id>/', views.project_settings, name='project_settings'),
]