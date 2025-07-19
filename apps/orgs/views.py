from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse

from .models import Organization
from .forms import OrganizationForm, OrgStatusForm
from apps.projects.models import Project


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
def delete_org(request, id):
    org = get_object_or_404(Organization, pk=id)
    
    context = {
        'org': org,
    }

    return render(request, 'dashboard/orgs/partials/org_delete_partial.html', context)


@login_required
def delete_org_confirm(request, id):
    org = get_object_or_404(Organization, pk=id)

    if request.user != org.owner:
        return HttpResponseForbidden()
    
    context = {
        'obj': org,
        'obj_delete_url': reverse('orgs:delete_org_confirm', kwargs={'id': org.pk}),
    }

    if request.method == 'POST':
        if 'password' in request.POST:
            check = request.user.check_password(request.POST.get('password'))
            if check:
                org.delete()

                messages.success(request, 'Organization was permanently deleted.')

                return redirect('dashboard:orgs')
            else:
                context['error'] = 'Incorrect password.'

                return render(request, 'dashboard/confirm_deletion.html', context)

    return render(request, 'dashboard/confirm_deletion.html', context)


@login_required
def org_settings(request, slug):
    org = get_object_or_404(Organization, slug=slug)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=org)
        if form.is_valid():
            form.save()

            messages.success(request, 'Organization was updated.')

            return redirect('dashboard:orgs')
    else:
        form = OrganizationForm(instance=org)
    
    context = {
        'org': org,
        'form': form,
    }
    
    return render(request, 'dashboard/orgs/org_settings.html', context)


@login_required
def change_org_status(request, id):
    org = get_object_or_404(Organization, pk=id)

    if request.method == 'POST':
        form = OrgStatusForm(request.POST, instance=org)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Organization status was changed!')
            return redirect('orgs:org_settings', org.id)
    else:
        form = OrgStatusForm(instance=org)

    context = {
        'org': org,
        'form': form,
    }

    return render(request, 'dashboard/orgs/partials/org_status_partial.html', context)


@login_required
def org_overview(request, id):
    org = get_object_or_404(Organization, pk=id)
    
    context = {
        'org': org,
    }

    return render(request, 'dashboard/orgs/partials/org_overview_partial.html', context)


@login_required
def org_details(request, slug):
    org = get_object_or_404(Organization, slug=slug)
    projects = org.projects.all()
    members = org.members.all()

    context = {
        'org': org,
        'projects': projects,
        'members': members,
    }

    return render(request, 'dashboard/orgs/org_details.html', context)
