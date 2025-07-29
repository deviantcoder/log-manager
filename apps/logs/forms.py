from django import forms

from .models import LogSource


class LogSourceForm(forms.ModelForm):
    class Meta:
        model = LogSource
        fields = ('name', 'description', 'source_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'placeholder': 'Enter source name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Add source description'})
