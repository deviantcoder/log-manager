from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse

from .models import Project, ProjectMember
from .forms import ProjectCreateForm, ProjectEditForm, ProjectStatusForm, AddProjectMemberForm
from .filters import ProjectFilter

from apps.orgs.models import Organization


@login_required
def projects_list(request):
    projects_filter = ProjectFilter(
        request.GET,
        queryset=Project.objects.filter(members__user=request.user),
        request=request
    )

    context = {
        'projects': projects_filter.qs,
        'filter': projects_filter,
    }

    if request.htmx:
        return render(request, 'dashboard/projects/partials/project_list.html', context={'projects': projects_filter.qs})

    return render(request, 'dashboard/projects/projects.html', context)


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()

            messages.success(request, 'Project created.')

            return redirect('projects:projects_list')
    else:
        form = ProjectCreateForm()

    context = {
        'form': form,
    }

    return render(request, 'dashboard/projects/project_form.html', context)


@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, pk=id)

    context = {
        'project': project,
    }

    return render(request, 'dashboard/projects/partials/project_delete_partial.html', context)


@login_required
def delete_project_confirm(request, org_slug, project_slug):
    project = get_object_or_404(Project, org__slug=org_slug, slug=project_slug)

    if request.user != project.created_by:
        return HttpResponseForbidden()
    
    context = {
        'obj': project,
        'obj_delete_url': reverse('projects:delete_project_confirm', kwargs={'org_slug': project.org.slug, 'project_slug': project.slug}),
    }

    if request.method == 'POST':
        if 'password' in request.POST:
            check = request.user.check_password(request.POST.get('password'))
            if check:
                project.delete()

                messages.success(request, 'Project was permanently deleted.')

                return redirect('projects:projects_list')
            else:
                context['error'] = 'Incorrect password.'

                return render(request, 'dashboard/confirm_deletion.html', context)

    return render(request, 'dashboard/confirm_deletion.html', context)



@login_required
def project_settings(request, org_slug, project_slug):
    project = get_object_or_404(Project, org__slug=org_slug, slug=project_slug)
    form = ProjectEditForm(instance=project)

    if request.method == 'POST':
        form = ProjectEditForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Project was updated.')

            return redirect('projects:projects_list')

    context = {
        'form': form,
        'project': project,
    }

    return render(request, 'dashboard/projects/project_settings.html', context)


@login_required
def change_project_status(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == 'POST':
        form = ProjectStatusForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.warning(request, 'Project status was changed!')
            return redirect(request.META.get('HTTP_REFERER') or 'projects:projects_list')
    else:
        form = ProjectStatusForm(instance=project)

    context = {
        'project': project,
        'form': form,
    }

    return render(request, 'dashboard/projects/partials/project_status_partial.html', context)


@login_required
def project_overview(request, id):
    project = get_object_or_404(Project, pk=id)
    
    context = {
        'project': project,
    }

    return render(request, 'dashboard/projects/partials/project_overview_partial.html', context)


@login_required
def project_details(request, org_slug, project_slug):
    project = get_object_or_404(Project, org__slug=org_slug, slug=project_slug)
    members = project.members.select_related('user')

    is_project_admin = any(
        m.user == request.user and m.role == ProjectMember.ROLE_CHOICES.ADMIN for m in members
    )

    context = {
        'project': project,
        'members': members,
        'is_admin': is_project_admin,
    }

    return render(request, 'dashboard/projects/project_details.html', context)


@login_required
def add_project_member(request, org_slug, project_slug):
    org = get_object_or_404(Organization, slug=org_slug)
    project = get_object_or_404(Project, org__slug=org_slug, slug=project_slug)
    
    if request.method == 'POST':
        form = AddProjectMemberForm(request.POST, org=org, project=project)
        if form.is_valid():
            member = form.save(commit=False)
            member.project = project
            member.save()

            messages.success(request, 'New member was added to the project team')

            return redirect('projects:project_details', org_slug=org.slug, project_slug=project.slug)
    else:
        form = AddProjectMemberForm(org=org, project=project)

    context = {
        'form': form,
        'project': project,
    }

    return render(request, 'dashboard/projects/partials/project_add_member.html', context)
