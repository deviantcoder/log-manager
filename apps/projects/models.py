from shortuuid import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from apps.orgs.models import Organization


User = get_user_model()


class Project(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = ('active', 'Active')
        INACTIVE = ('inactive', 'Inactive')
        ARCHIVED = ('archived', 'Archived')

    name = models.CharField(max_length=100)
    slug = models.SlugField()
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    description = models.TextField(max_length=500, null=True, blank=True)

    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('org', 'slug')
        ordering = ('status', '-created',)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            base_slug = slugify(self.name)
            self.slug = base_slug

            if Project.objects.filter(org=self.org, slug__iexact=base_slug).exists():
                self.slug = f'{base_slug}-{str(uuid())}'[:50]
        super().save(*args, **kwargs)


class ProjectMember(models.Model):
    class ROLE_CHOICES(models.TextChoices):
        ADMIN = ('admin', 'Admin')
        MEMBER = ('member', 'Member')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES.choices, default=ROLE_CHOICES.MEMBER
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f'{self.user}: {self.project} ({self.role})'
