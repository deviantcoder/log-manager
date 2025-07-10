from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Project, ProjectMember


@receiver(post_save, sender=Project)
def create_creator_membership(sender, instance, created, **kwargs):
    if created:
        ProjectMember.objects.create(
            user=instance.created_by,
            project=instance,
            role=ProjectMember.ROLE_CHOICES.ADMIN
        )
