from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.urls import reverse

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
def delete_org(request, id):
    org = get_object_or_404(Organization, pk=id)
    context = {
        'obj': org,
        'obj_name': 'organization',
        'delete_confirm_url': reverse('orgs:delete_org_confirm', kwargs={'id': org.pk}),
    }
    return render(request, 'dashboard/partials/modal_partial.html', context)


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
def org_settings(request, id):
    org = get_object_or_404(Organization, pk=id)

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
