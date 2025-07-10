from django.contrib import admin
from .models import Organization, OrgMember


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    model = OrgMember
