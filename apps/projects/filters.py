import django_filters

from .models import Project


class ProjectFilter(django_filters.FilterSet):
    project_status = django_filters.ChoiceFilter(
        choices=Project.StatusChoices.choices,
        field_name='status',
        lookup_expr='iexact',
        empty_label='Any',
    )

    class Meta:
        model = Project
        fields = ('status',)