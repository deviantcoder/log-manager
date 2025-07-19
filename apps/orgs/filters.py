import django_filters

from .models import Organization


class OrgFilter(django_filters.FilterSet):
    org_status = django_filters.ChoiceFilter(
        choices=Organization.StatusChoices.choices,
        field_name='status',
        lookup_expr='iexact',
        empty_label='Any',
    )

    class Meta:
        model = Organization
        fields = (
            'status',
        )
