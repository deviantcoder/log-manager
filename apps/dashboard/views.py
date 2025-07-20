from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.projects.models import Project

from apps.orgs.models import Organization
from apps.orgs.filters import OrgFilter


@login_required
def dashboard(request):
    orgs = Organization.objects.filter(members__user=request.user, status=Organization.StatusChoices.ACTIVE)
    projects = Project.objects.filter(members__user=request.user, status=Project.StatusChoices.ACTIVE)
    context = {
        'orgs': orgs[:2],
        'projects': projects[:2],
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')
