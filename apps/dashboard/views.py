from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.projects.models import Project


@login_required
def dashboard(request):
    orgs = request.user.owned_orgs.all()
    projects = Project.objects.filter(projectmember__user=request.user, status=Project.StatusChoices.ACTIVE)
    context = {
        'orgs': orgs[:2],
        'projects': projects[:2],
    }
    return render(request, 'dashboard/dashboard.html', context)


@login_required
def organizations(request):
    user_orgs = request.user.owned_orgs.all()
    context = {
        'orgs': user_orgs,
    }
    return render(request, 'dashboard/orgs/orgs.html', context)


@login_required
def projects(request):
    projects = Project.objects.filter(projectmember__user=request.user, status=Project.StatusChoices.ACTIVE)
    context = {
        'projects': projects
    }
    return render(request, 'dashboard/projects/projects.html', context)
