from shortuuid import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


User = get_user_model()


class Organization(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_orgs')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            base_slug = slugify(self.name)
            self.slug = base_slug

            if Organization.objects.filter(slug__iexact=base_slug).exists():
                self.slug = f'{base_slug}-{str(uuid())}'[:50]
        super().save(*args, **kwargs)
