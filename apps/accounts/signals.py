from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import compress_image


User = get_user_model()


@receiver(pre_save, sender=User)
def compress_user_image(sender, instance, **kwargs):
    if not instance.image:
        return
    
    try:
        if instance.pk:
            old_image = User.objects.filter(pk=instance.pk).values_list('image', flat=True).first()
            if old_image and old_image == instance.image:
                return
    except Exception as e:
        pass # TODO: add logging here

    try:
        instance.image = compress_image(instance.image)
    except Exception as e:
        pass # TODO: add logging here
