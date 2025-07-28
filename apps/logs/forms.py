from django import forms

from .models import LogSource


class LogSourceForm(forms.ModelForm):
    class Meta:
        model = LogSource
        fields = ('name', 'description', 'source_type')
