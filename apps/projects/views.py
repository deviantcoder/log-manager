from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse

from .models import Project
from .forms import ProjectCreateForm, ProjectEditForm, ProjectStatusForm


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectCreateForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()

            messages.success(request, 'Project created.')

            return redirect('dashboard:projects')
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
def delete_project_confirm(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.user != project.created_by:
        return HttpResponseForbidden()
    
    context = {
        'obj': project,
        'obj_delete_url': reverse('projects:delete_project_confirm', kwargs={'id': project.pk}),
    }

    if request.method == 'POST':
        if 'password' in request.POST:
            check = request.user.check_password(request.POST.get('password'))
            if check:
                project.delete()

                messages.success(request, 'Project was permanently deleted.')

                return redirect('dashboard:projects')
            else:
                context['error'] = 'Incorrect password.'

                return render(request, 'dashboard/confirm_deletion.html', context)

    return render(request, 'dashboard/confirm_deletion.html', context)



@login_required
def project_settings(request, id):
    project = get_object_or_404(Project, pk=id)
    form = ProjectEditForm(instance=project)

    if request.method == 'POST':
        form = ProjectEditForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Project was updated.')

            return redirect('dashboard:projects')

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
            return redirect('projects:project_settings', project.id)
    else:
        form = ProjectStatusForm()

    context = {
        'project': project,
        'form': form,
    }

    return render(request, 'dashboard/projects/partials/project_status_partial.html', context)
