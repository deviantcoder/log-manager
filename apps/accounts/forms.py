import re

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from .utils import send_verification_email


User = get_user_model()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your username or email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter your password'})


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name', 'image', 'password1', 'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter your email'})
        self.fields['username'].widget.attrs.update({'placeholder': 'Create a username'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your first name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Enter your last name'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repeat the password'})

    def save(self, commit=True):
        user = super().save(commit=False)

        user.is_active = False

        if commit:
            user.save()
            send_verification_email(user)

        return user


class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
    
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not re.match(r'^[a-zA-Z0-9.]+$', username):
            raise ValidationError('Username can only contain English letters, numbers, and periods.')

        if len(username) < 5 or len(username) > 25:
            raise ValidationError('Username must be between 5 and 25 characters.')

        if username == self.current_user.username:
            raise ValidationError('This is already your username.')
        
        if User.objects.filter(username=username).exclude(pk=self.current_user.pk).exists():
            raise ValidationError('This username is already taken.')
        
        return username
