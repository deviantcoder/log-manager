from django.contrib import admin
from .models import Organization, OrgMember, Project


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    model = OrgMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
