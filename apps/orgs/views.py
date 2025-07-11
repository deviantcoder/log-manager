from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Organization
from .forms import OrganizationForm


@login_required
def create_org(request):

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.owner = request.user
            org.save()
            messages.success(request, 'Organization created.')
            return redirect('dashboard:orgs')
    else:
        form = OrganizationForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/orgs/org_form.html', context)


@login_required
def org_settings(request, id):
    org = Organization.objects.filter(id=id).first()

    print(org)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            messages.success(request, 'Organization updated.')
            return redirect('dashboard:orgs')
    else:
        form = OrganizationForm(instance=org)
    context = {
        'org': org,
        'form': form,
    }
    return render(request, 'dashboard/orgs/org_settings.html', context)
