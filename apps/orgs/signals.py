import logging

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Organization, OrgMember

from utils.images import compress_image


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Organization)
def create_owner_membership(sender, instance, created, **kwargs):
    if created:
        OrgMember.objects.create(
            user=instance.owner,
            org=instance,
            role=OrgMember.ROLE_CHOICES.ADMIN
        )


@receiver(pre_save, sender=Organization)
def compress_org_image(sender, instance, **kwargs):
    if not instance.image:
        return
    
    try:
        if instance.pk:
            old_image = Organization.objects.filter(pk=instance.pk).values_list('image', flat=True).first()
            if old_image and old_image == instance.image:
                return
    except Exception as e:
        logging.warning(f'Image compression failed: {e}')

    try:
        instance.image = compress_image(instance.image)
    except Exception as e:
        logging.warning(f'Image compression failed: {e}')
