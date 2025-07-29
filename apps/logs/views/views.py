from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.http import HttpResponse
from django.urls import reverse

from apps.logs.forms import LogSourceForm
from apps.logs.models import LogSource

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


@login_required
def log_source_overview(request, source_id):
    source = get_object_or_404(LogSource, pk=source_id)

    context = {
        'source': source,
    }

    return render(request, 'dashboard/logs/partials/log_source_overview_partial.html', context)


@login_required
def delete_log_source(request, source_id):
    source = get_object_or_404(LogSource, pk=source_id)

    context = {
        'source': source,
    }

    return render(request, 'dashboard/logs/partials/log_source_delete_partial.html', context)

@login_required
def delete_log_source_confirm(request, source_id):
    source = get_object_or_404(LogSource, pk=source_id)

    if request.method == 'POST':
        if 'password' in request.POST:
            check = request.user.check_password(request.POST.get('password'))
            if check:
                source.delete()

                messages.success(request, 'Source was permanently deleted.')
            
                response = HttpResponse()
                response['HX-Redirect'] = reverse(
                    'projects:project_details',
                    kwargs={'org_slug': source.project.org.slug, 'project_slug': source.project.slug}
                )
                return response
            else:
                context = {
                    'source': source,
                    'error': 'Incorrect password.'
                }

                return render(request, 'dashboard/logs/partials/log_source_delete_confirm_partial.html', context)

    context = {
        'source': source,
    }

    return render(request, 'dashboard/logs/partials/log_source_delete_confirm_partial.html', context)
