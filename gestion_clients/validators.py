import os
from io import BytesIO

from PIL import Image
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', '.gif',
                        '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm']
    if not ext.lower() in valid_extensions:
        raise ValidationError(_('unsupported file extension'))


def validate_type(value):
    var = value.content_type == "application/pdf" or value.content_type.startswith("image/")
    if not var:
        raise ValidationError(
            _('%(value)s files are not supported'),
            params={'value': value.content_type},
        )
    if value.content_type.startswith("image/"):
        img = Image.open(value.file)
        img = img.convert('RGB')
        byte_io = BytesIO()
        img.save(byte_io, 'PDF')
        value.file = byte_io
        value.content_type = "application/pdf"
        img.close()
