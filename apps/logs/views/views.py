from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.logs.forms import LogSourceForm
from apps.projects.models import Project


@login_required
def create_log_source(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == 'POST':
        form = LogSourceForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            
            source.project = project
            source.created_by = request.user
            source.save()

            messages.success(request, 'New source was added.')

            return redirect('projects:project_details', project.org.slug, project.slug)
    else:
        form = LogSourceForm()

    context = {
        'form': form,
        'project': project,
    }

    return render(request, 'dashboard/logs/partials/log_source_form_partial.html', context)
