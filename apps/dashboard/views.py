from django.shortcuts import render


def dashboard(request):
    user_orgs = request.user.owned_orgs.all()
    context = {
        'owned_orgs': user_orgs[:2],
    }
    return render(request, 'dashboard/dashboard.html', context)


def organizations(request):
    user_orgs = request.user.owned_orgs.all()
    context = {
        'owned_orgs': user_orgs,
    }
    return render(request, 'dashboard/orgs.html', context)


def projects(request):
    context = {}
    return render(request, 'dashboard/projects.html', context)
