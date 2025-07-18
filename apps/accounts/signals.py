import os
import shutil
import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from utils.images import compress_image


User = get_user_model()
logger = logging.getLogger(__name__)


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
        logging.warning(f'Image compression failed: {e}')

    try:
        instance.image = compress_image(instance.image)
    except Exception as e:
        logging.warning(f'Image compression failed: {e}')


@receiver(post_delete, sender=User)
def delete_user_media(sender, instance, **kwargs):
    try:
        path = f'media/accounts/{str(instance.public_id)[:8]}'
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception as e:
        logger.warning(f'User media deletion failed: {e}')
