from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('settings/', views.account_settings_view, name='settings')
]