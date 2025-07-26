from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.projects.models import Project

from apps.orgs.models import Organization, OrgInvite
from apps.orgs.filters import OrgFilter


@login_required
def dashboard(request):
    orgs = Organization.objects.filter(members__user=request.user, status=Organization.StatusChoices.ACTIVE)
    projects = Project.objects.filter(members__user=request.user, status=Project.StatusChoices.ACTIVE)
    context = {
        'orgs': orgs[:2],
        'projects': projects[:2],
        'orgs_count': orgs.count(),
        'projects_count': projects.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def settings_view(request):
    return render(request, 'dashboard/settings.html')


@login_required
def inbox(request):
    pending_invites = OrgInvite.objects.filter(
        is_existing_user=True,
        email=request.user.email,
        accepted=False,
        declined=False
    )

    context = {
        'pending_invites': pending_invites,
    }

    return render(request, 'dashboard/inbox.html', context)
