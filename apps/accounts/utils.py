import os
import logging

from PIL import Image
from io import BytesIO

from django.core.files import File


logger = logging.getLogger(__name__)


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
