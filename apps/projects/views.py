from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ProjectForm


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            messages.success(request, 'Project created.')
            return redirect('dashboard:projects')
    else:
        form = ProjectForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/projects/project_form.html', context)
