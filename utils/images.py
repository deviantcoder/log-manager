import os
import logging
import shortuuid

from PIL import Image
from io import BytesIO

from django.core.files import File


logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif', 'webp')


def upload_to(instance, filename, base_dir='uploads', id_attr='public_id'):
    ext = os.path.splitext(filename)[-1].lower()
    new_filename = shortuuid.uuid()

    obj_id = getattr(instance, id_attr, None) or getattr(instance, 'pk', 'unknown')

    return f'{base_dir}/{str(obj_id)[:8]}/{new_filename}{ext}'


def compress_image(file):
    try:
        with Image.open(file) as image:
            if image.mode in ('P', 'RGBA'):
                image = image.convert('RGB')
            
            image_io = BytesIO()
            name = os.path.splitext('file')[0] + '.jpg'
            image.save(image_io, format='JPEG', quality=60, optimize=True)

            return File(image_io, name=name)

    except Exception as e:
        logger.warning(f'Image compression failed: {e}')
