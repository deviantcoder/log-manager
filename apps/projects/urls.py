from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('projects/', views.projects_list, name='projects_list'),

    path('projects/create/', views.create_project, name='create_project'),
    path('projects/delete/<str:id>/', views.delete_project, name='delete_project'),
    path('organizations/<slug:org_slug>/projects/<slug:project_slug>/delete/confirm/', views.delete_project_confirm, name='delete_project_confirm'),
    path('projects/change-status/<str:id>/', views.change_project_status, name='change_project_status'),

    path('organizations/<slug:org_slug>/projects/<slug:project_slug>/settings/', views.project_settings, name='project_settings'),

    path('projects/overview/<str:id>/', views.project_overview, name='project_overview'),
    path('organizations/<slug:org_slug>/projects/<slug:project_slug>/', views.project_details, name='project_details'),
]