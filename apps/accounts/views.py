import re
import logging

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.views import generic
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse_lazy

from .forms import LoginForm, SignupForm, UsernameUpdateForm
from .utils import send_verification_email

from apps.orgs.models import OrgInvite, OrgMember


logger = logging.getLogger(__name__)

User = get_user_model()


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard:dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = self.request.user

        if user is not None:
            if user.email_verified:
                messages.success(self.request, 'Welcome back!')
                return redirect(self.get_success_url())
            else:
                sent = send_verification_email(user)
                return render(self.request, 'email_verification/verify_email_sent.html', context={'sent': sent})
        else:
            messages.warning(self.request, 'Invalid email, username or password.')
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Invalid email, username or password.')
        return super().form_invalid(form)


class LogoutUserView(LogoutView):
    pass


class SignupUserView(generic.CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('dashboard:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        response = super().form_valid(form)

        user = form.instance

        if user is not None:
            if 'invite_token' in self.request.session:
                token = self.request.session.get('invite_token')
                invite = get_object_or_404(OrgInvite, token=token)

                invite.accepted = True
                invite.save(update_fields=['accepted'])

                user.email_verified = True
                user.save(update_fields=['email_verified'])

                OrgMember.objects.create(org=invite.org, user=user)
                
                try:
                    del self.request.session['invite_token']
                except KeyError:
                    logger.warning(f'No invite_token in session for {user}')
                    
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(self.request, user)
                messages.success(self.request, f'You have joined {invite.org.name}')

                return redirect(self.get_success_url())
            else:
                send_verification_email(user)

                return render(
                    self.request,
                    'email_verification/verify_email_sent.html',
                    context={'sent': True}
                )
        
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


@login_required
def check_username(request):
    LOWER_LIMIT = 5
    UPPER_LIMIT = 25

    pattern = r'^[a-zA-Z0-9_]+$'

    username = request.GET.get('username', '').strip()

    context = {
        'available': True,
        'msg': '',
    }

    if username:
        if len(username) < LOWER_LIMIT:
            context['available'] = False
            context['msg'] = 'Too short (min 5 characters)'

        if len(username) > UPPER_LIMIT:
            context['available'] = False
            context['msg'] = 'Too long (max 25 characters)'

        if not re.match(pattern, username):
            context['available'] = False
            context['msg'] = 'Invalid characters. Only letters, digits and underscores allowed.'

        if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            context['available'] = False
            context['msg'] = 'Username is already taken'
    else:
        context['available'] = False
        context['msg'] = 'Username cannot be empty'

    return render(request, 'accounts/partials/check_username.html', context)


def verify_email(request, uidb64, token):
    if request.user.is_authenticated and request.user.email_verified:
        return redirect('dashboard:dashboard')

    token_generator = PasswordResetTokenGenerator()

    try:
        public_id_bytes = urlsafe_base64_decode(uidb64)
        public_id = public_id_bytes.decode('utf-8')

        user = get_object_or_404(User, public_id=public_id)

    except Exception as e:
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.email_verified = True

        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        messages.success(request, 'Successfully activated your account.')

        return redirect('dashboard:dashboard')
    
    return render(request, 'email_verification/verify_email_failed.html')
