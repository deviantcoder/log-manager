from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('settings/', views.account_settings_view, name='settings'),
    path('check-username/', views.check_username, name='check_username'),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
]