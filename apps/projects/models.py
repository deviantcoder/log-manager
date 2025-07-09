from django.db import models
from apps.orgs.models import Organization


class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    description = models.TextField(max_length=500, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('org', 'slug')

    def __str__(self):
        return self.name
