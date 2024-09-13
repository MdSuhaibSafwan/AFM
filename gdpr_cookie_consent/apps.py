from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GdprCookieConsentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gdpr_cookie_consent"
    verbose_name = _("GDPR Cookie Consent")
