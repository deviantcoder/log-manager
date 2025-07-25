import logging
import django_filters

from .models import Project, ProjectMember


logger = logging.getLogger(__name__)


class ProjectFilter(django_filters.FilterSet):
    
    project_status = django_filters.ChoiceFilter(
        choices=Project.StatusChoices.choices,
        field_name='status',
        lookup_expr='iexact',
        empty_label='Any',
    )

    user_role = django_filters.ChoiceFilter(
        label='role',
        choices=ProjectMember.ROLE_CHOICES.choices,
        method='filter_by_user_role',
        empty_label='Any',
    )

    class Meta:
        model = Project
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        try:
            request = kwargs.pop('request')
            self.user = request.user
        except KeyError as e:
            logger.warning(e)

        super().__init__(*args, **kwargs)

    def filter_by_user_role(self, queryset, name, value):
        if value == ProjectMember.ROLE_CHOICES.ADMIN:
            return queryset.filter(members__user=self.user, members__role=ProjectMember.ROLE_CHOICES.ADMIN)
        elif value == ProjectMember.ROLE_CHOICES.MEMBER:
            return queryset.filter(members__user=self.user, members__role=ProjectMember.ROLE_CHOICES.MEMBER)

        return queryset
