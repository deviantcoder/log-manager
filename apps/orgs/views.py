from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponseForbidden
from django.urls import reverse

from .models import Organization, OrgInvite, OrgMember
from .forms import OrganizationForm, OrgStatusForm, OrgInviteForm
from .filters import OrgFilter
from .utils import send_invite_email

from apps.projects.models import Project


User = get_user_model()


@login_required
def orgs_list(request):
    orgs_filter = OrgFilter(
        request.GET,
        queryset=Organization.objects.filter(members__user=request.user),
        request=request
    )

    context = {
        'orgs': orgs_filter.qs,
        'filter': orgs_filter,
    }

    if request.htmx:
        return render(request, 'dashboard/orgs/partials/org_list.html', context={'orgs': orgs_filter.qs})

    return render(request, 'dashboard/orgs/orgs.html', context)


@login_required
def create_org(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.owner = request.user
            org.save()
            messages.success(request, 'Organization created.')
            return redirect('orgs:orgs_list')
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

                return redirect('orgs:orgs_list')
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
            return redirect(request.META.get('HTTP_REFERER') or 'orgs:orgs_list')
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
    active_projects_count = projects.filter(status=Project.StatusChoices.ACTIVE).count()
    available_projects = projects.filter(members__user=request.user)
    
    members = org.members.select_related('user')

    is_org_admin = any(
        m.user.id == request.user.id and m.role == OrgMember.ROLE_CHOICES.ADMIN for m in members
    )

    context = {
        'org': org,
        'available_projects': available_projects,
        'active_projects_count': active_projects_count,
        'members': members,
        'is_admin': is_org_admin,
    }

    return render(request, 'dashboard/orgs/org_details.html', context)


@login_required
def invite_member(request, id):
    org = get_object_or_404(Organization, pk=id)
    form = OrgInviteForm()

    if request.user != org.owner:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = OrgInviteForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')

            if request.user.email == email:
                messages.warning(request, 'You cannot send an invitation to yourself.')
                return redirect(request.META.get('HTTP_REFERER') or 'orgs:orgs_list')

            if User.objects.filter(email=email).exclude(pk=request.user.pk).exists():
                invite = form.save(commit=False)

                invite.org = org
                invite.invited_by = request.user
                invite.is_existing_user = True

                invite.save()               # TODO: Notify user in inbox (future feature)

                messages.success(request, 'Sent an invitation.')
            else:
                invite = form.save(commit=False)

                invite.org = org
                invite.invited_by = request.user
                invite.is_existing_user = False

                invite.save()

                send_invite_email(invite)

                messages.success(request, 'Sent an email invitation.')

            return redirect(request.META.get('HTTP_REFERER') or 'orgs:orgs_list')

    context = {
        'form': form,
        'org': org,
    }

    return render(request, 'dashboard/orgs/partials/org_invite_form_partial.html', context)


def accept_invite(request, token):
    invite = get_object_or_404(
        OrgInvite, token=token, accepted=False, declined=False
    )

    if invite.is_existing_user:
        if request.method == 'POST':
            
            if 'accept_invite' in request.POST:
                invite.accepted = True
                invite.save(update_fields=['accepted'])

                OrgMember.objects.get_or_create(
                    user=request.user,
                    org=invite.org,
                )

                return redirect('orgs:org_details', invite.org.slug)

            elif 'decline_invite' in request.POST:
                invite.declined = True
                invite.save(update_fields=['declined'])

                return redirect(request.META.get('HTTP_REFERER') or 'dashboard:inbox')
    else:
        request.session['invite_token'] = str(invite.token)
        return redirect('accounts:signup')
