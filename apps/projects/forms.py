from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'org', 'name', 'description'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter project name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Add a description'})
