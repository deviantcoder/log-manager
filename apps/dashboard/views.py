from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.projects.models import Project
from apps.orgs.models import Organization


@login_required
def dashboard(request):
    orgs = Organization.objects.filter(orgmember__user=request.user, status=Organization.StatusChoices.ACTIVE)
    projects = Project.objects.filter(projectmember__user=request.user, status=Project.StatusChoices.ACTIVE)
    context = {
        'orgs': orgs[:2],
        'projects': projects[:2],
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def organizations(request):
    orgs = Organization.objects.filter(orgmember__user=request.user)
    context = {
        'orgs': orgs,
    }
    return render(request, 'dashboard/orgs/orgs.html', context)


@login_required
def projects(request):
    projects = Project.objects.filter(projectmember__user=request.user)
    context = {
        'projects': projects
    }
    return render(request, 'dashboard/projects/projects.html', context)
