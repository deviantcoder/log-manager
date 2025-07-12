from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Project
from .forms import ProjectCreateForm, ProjectEditForm


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
