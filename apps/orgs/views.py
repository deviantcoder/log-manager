from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

    form = OrganizationForm()
    context = {
        'form': form,
    }
    return render(request, 'dashboard/orgs/org_form.html', context)
