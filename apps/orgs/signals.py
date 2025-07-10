from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Organization, OrgMember


@receiver(post_save, sender=Organization)
def create_owner_membership(sender, instance, created, **kwargs):
    if created:
        OrgMember.objects.create(
            user=instance.owner,
            org=instance,
            role=OrgMember.ROLE_CHOICES.ADMIN
        )