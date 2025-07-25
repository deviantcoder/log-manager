import logging

from django import forms
from django.contrib.auth import get_user_model

from .models import Project, ProjectMember

from apps.orgs.models import Organization


logger = logging.getLogger(__name__)

User = get_user_model()


class BaseProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'org', 'name', 'description'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Enter project name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Add a description'})


class ProjectCreateForm(BaseProjectForm):
    pass


class ProjectEditForm(BaseProjectForm):
    class Meta(BaseProjectForm.Meta):
        fields = ('name', 'description')


class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('status',)


class AddProjectMemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=None, label='Organization Member')

    class Meta:
        model = ProjectMember
        fields = ('user', 'role')

    def __init__(self, *args, **kwargs):
        org = kwargs.pop('org', None)
        project = kwargs.pop('project', None)

        super().__init__(*args, **kwargs)

        if org and project:
            org_members = org.members.all()
            project_members_pks = project.members.values_list('user__pk', flat=True)

            self.fields['user'].queryset = User.objects.filter(
                pk__in=org_members.values_list('user__pk', flat=True)
            ).exclude(id__in=project_members_pks)
