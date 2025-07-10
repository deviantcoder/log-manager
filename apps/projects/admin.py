from django.contrib import admin
from .models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project
    list_display = ('name', 'org', 'created_by', 'status')
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
    

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    model = ProjectMember
