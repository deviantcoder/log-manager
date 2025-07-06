from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.views import generic
from django.contrib import messages

from .forms import LoginForm, SignupForm, UsernameUpdateForm


User = get_user_model()


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
    

@login_required
def account_settings_view(request):
    user = request.user
    if request.method == 'POST':
        if 'update_image' in request.POST:
            new_image = request.FILES.get('image')
            if new_image:
                user.image = new_image
                user.save()
                messages.success(request, 'Profile image changed.')

        if 'update_username' in request.POST:
            form = UsernameUpdateForm(request.POST, current_user=user, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Username updated.')
            else:
                for error in form.errors.values():
                    messages.warning(request, error)

        return redirect('accounts:settings')

    context = {}
    return render(request, 'accounts/account_settings.html', context)
