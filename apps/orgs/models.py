from shortuuid import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_organizations')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            base_slug = slugify(self.name)
            self.slug = base_slug
            if Organization.objects.filter(slug__iexact=base_slug).exists():
                self.slug = f'{base_slug}-{uuid()[:8]}'[:50]
        super().save(*args, **kwargs)


class OrgMember(models.Model):
    class ROLE_CHOICES(models.TextChoices):
        ADMIN = ('admin', 'Admin')            
        MEMBER = ('member', 'Member')   

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=6, choices=ROLE_CHOICES.choices, default=ROLE_CHOICES.MEMBER
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return self.user
    

class Project(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    description = models.TextField(max_length=500, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('organization', 'slug')

    def __str__(self):
        return self.name
