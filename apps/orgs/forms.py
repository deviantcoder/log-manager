from django import forms

from .models import Organization


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
