from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_file_size(value):
    if value:
        if value.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(_('Please keep filesize under %s. Current filesize is %s') % (
            filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(value.size)))