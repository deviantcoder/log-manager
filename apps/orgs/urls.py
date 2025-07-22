from django.urls import path
from . import views

app_name = 'orgs'

urlpatterns = [
    path('', views.orgs_list, name='orgs_list'),
    path('create/', views.create_org, name='create_org'),
    path('settings/<slug:slug>/', views.org_settings, name='org_settings'),
    path('delete/<str:id>/', views.delete_org, name='delete_org'),
    path('delete/<str:id>/confirm/', views.delete_org_confirm, name='delete_org_confirm'),
    path('change-status/<str:id>/', views.change_org_status, name='change_org_status'),
    path('overview/<str:id>/', views.org_overview, name='org_overview'),
    path('<str:id>/invite-member/', views.invite_member, name='invite_member'),
    path('accept-invite/<str:token>', views.accept_invite, name='accept_invite'),

    path('<slug:slug>/', views.org_details, name='org_details'),
]