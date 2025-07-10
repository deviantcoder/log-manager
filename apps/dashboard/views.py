from django.shortcuts import render

from apps.projects.models import Project


def dashboard(request):
    orgs = request.user.owned_orgs.all()
    projects = Project.objects.filter(projectmember__user=request.user, status=Project.StatusChoices.ACTIVE)
    context = {
        'owned_orgs': orgs[:2],
        'projects': projects[:2],
    }
    return render(request, 'dashboard/dashboard.html', context)


def organizations(request):
    user_orgs = request.user.owned_orgs.all()
    context = {
        'owned_orgs': user_orgs,
    }
    return render(request, 'dashboard/orgs.html', context)


def projects(request):
    projects = Project.objects.filter(projectmember__user=request.user)
    context = {
        'projects': projects
    }
    return render(request, 'dashboard/projects.html', context)
