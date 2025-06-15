from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages

from .forms import LoginForm


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True # change to True after testing

    def form_valid(self, form):
        messages.success(self.request, 'Welcome back!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if '__all__' in form.errors:
            messages.warning(self.request, 'Invalid username or password')
        return super().form_invalid(form)
