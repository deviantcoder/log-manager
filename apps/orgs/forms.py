from django import forms
from django.core.validators import EmailValidator

from .models import Organization, OrgInvite


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = (
            'name', 'description'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter organization name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Add a description'})


class OrgStatusForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ('status',)


class OrgInviteForm(forms.ModelForm):
    class Meta:
        model = OrgInvite
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'johndoe@gmail.com'})
