import os
import shortuuid

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

from .utils import compress_image


ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp')


def upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1].lower()
    new_filename = shortuuid.uuid()[:8]

    return f'accounts/{str(instance.public_id)[:8]}/{new_filename}{ext}'


class User(AbstractUser):
    username = models.CharField(max_length=25, unique=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)

    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to=upload_to,
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS)]
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    public_id = models.UUIDField(default=uuid4, unique=True, editable=False, db_index=True)

    class Meta:
        ordering = ('-created', 'username',)

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
    
    @property
    def image_or_default(self):
        if self.image:
            return self.image.url
        return 'static/img/def.png'
