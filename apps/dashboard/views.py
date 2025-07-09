from django.shortcuts import render


def dashboard(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)


def organizations(request):
    context = {}
    return render(request, 'dashboard/orgs.html', context)


def projects(request):
    context = {}
    return render(request, 'dashboard/projects.html', context)
