from django.shortcuts import render

from apps.projects.models import Project


def dashboard(request):
    orgs = request.user.owned_orgs.all()
    projects = Project.objects.filter(projectmember__user=request.user, status=Project.StatusChoices.ACTIVE)
    context = {
        'orgs': orgs[:2],
        'projects': projects[:2],
    }
    return render(request, 'dashboard/dashboard.html', context)


def organizations(request):
    user_orgs = request.user.owned_orgs.all()
    context = {
        'orgs': user_orgs,
    }
    return render(request, 'dashboard/orgs/orgs.html', context)


def projects(request):
    projects = Project.objects.filter(projectmember__user=request.user, status=Project.StatusChoices.ACTIVE)
    context = {
        'projects': projects
    }
    return render(request, 'dashboard/projects/projects.html', context)
