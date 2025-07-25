from django.contrib import admin
from .models import Organization, OrgMember, OrgInvite


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('name', 'owner', 'status', 'members')

    def members(self, obj):
        return obj.members.count()
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    model = OrgMember


@admin.register(OrgInvite)
class OrgInviteAdmin(admin.ModelAdmin):
    model = OrgInvite
    list_display = ('org', 'invited_by', 'email', 'accepted', 'declined', 'is_existing_user')
