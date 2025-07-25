import logging
import django_filters

from .models import Organization, OrgMember


logger = logging.getLogger(__name__)


class OrgFilter(django_filters.FilterSet):

    org_status = django_filters.ChoiceFilter(
        choices=Organization.StatusChoices.choices,
        field_name='status',
        lookup_expr='iexact',
        empty_label='Any',
    )

    user_role = django_filters.ChoiceFilter(
        label='role',
        choices=OrgMember.ROLE_CHOICES.choices,
        method='filter_by_user_role',
        empty_label='Any',
    )

    class Meta:
        model = Organization
        fields = (
            'status',
        )

    def __init__(self, *args, **kwargs):
        try:
            request = kwargs.pop('request')
            self.user = request.user
        except KeyError as e:
            logger.warning(e)

        super().__init__(*args, **kwargs)

    def filter_by_user_role(self, queryset, name, value):
        if value == OrgMember.ROLE_CHOICES.ADMIN:
            return queryset.filter(members__user=self.user, members__role=OrgMember.ROLE_CHOICES.ADMIN)
        elif value == OrgMember.ROLE_CHOICES.MEMBER:
            return queryset.filter(members__user=self.user, members__role=OrgMember.ROLE_CHOICES.MEMBER)

        return queryset
