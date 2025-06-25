from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import authenticate, login
from django.views import generic
from django.contrib import messages

from .forms import LoginForm, SignupForm


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'Welcome back!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if '__all__' in form.errors:
            messages.warning(self.request, 'Invalid email, username or password.')
        return super().form_invalid(form)


class LogoutUserView(LogoutView):
    pass


class SignupUserView(generic.CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)

        user = authenticate(
            request=self.request,
            username=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password1'),
        )
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'Signed up.')
        
        return response
    
    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.warning(self.request, f'{field.capitalize()}: {error}')
        return super().form_invalid(form)
