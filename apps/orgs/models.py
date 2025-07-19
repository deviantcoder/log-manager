from shortuuid import uuid
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

from utils.images import upload_to as base_upload_to, ALLOWED_EXTENSIONS


User = get_user_model()


def upload_to(instance, filename):
    return base_upload_to(instance, filename, base_dir='orgs')


class Organization(models.Model):
    class StatusChoices(models.TextChoices):
        ACTIVE = ('active', 'Active')
        INACTIVE = ('inactive', 'Inactive')
        ARCHIVED = ('archived', 'Archived')

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_orgs')

    description = models.TextField(max_length=500, null=True, blank=True)

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_to,
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS)]
    )

    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    public_id = models.UUIDField(default=uuid4, unique=True, editable=False, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            base_slug = slugify(self.name)
            self.slug = base_slug

            if Organization.objects.filter(slug__iexact=base_slug).exists():
                self.slug = f'{base_slug}-{str(uuid())}'[:50]
        super().save(*args, **kwargs)

    @property
    def image_or_default(self):
        if self.image:
            return self.image.url
        return '/static/img/default_org_logo.png'


class OrgMember(models.Model):
    class ROLE_CHOICES(models.TextChoices):
        ADMIN = ('admin', 'Admin')
        MEMBER = ('member', 'Member')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES.choices, default=ROLE_CHOICES.MEMBER
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'org')

    def __str__(self):
        return f'{self.user}: {self.org} ({self.role})'
