from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class CookieConsentRecord(models.Model):
    # Fields not used for verification hash
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    # Fields used for verification hash
    user_name = models.CharField(_("User Name"), max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(_("IP address"), blank=True, null=True)
    user_agent_string = models.TextField(_("User Agent String"), blank=True)
    timestamp = models.DateTimeField(_("Timestamp"), default=now)
    choices_provided = models.TextField(_("Choices provided"), blank=True)
    choices_accepted = models.TextField(_("Choices accepted"), blank=True)
    choices_json = models.TextField(_("Choices in JSON"), blank=True)
    # choices_json will be converted to models.JSONField, when Django 2.2, 3.0, 3.1 support is dropped
    verification_hash = models.CharField(
        _("Verification Hash"),
        max_length=32,
        help_text=_(
            "MD5 hash of this record, Django Secret Key, and the hash of previous log entry."
        ),
    )

    class Meta:
        verbose_name = _("Cookie Consent Record")
        verbose_name_plural = _("Cookie Consent Logs")

    def __str__(self):
        return f"{self.timestamp:%Y-%m-%d %H:%M}"

    def save(self, *args, **kwargs):
        if not self.verification_hash:
            self.calculate_verification_hash()
        super().save(*args, **kwargs)

    def calculate_verification_hash(self):
        import hashlib
        import json
        from django.core.serializers.json import DjangoJSONEncoder

        if self.pk:
            previous_log_entry = (
                CookieConsentRecord.objects.filter(pk__lt=self.pk).order_by("-pk").first()
            )
        else:
            previous_log_entry = CookieConsentRecord.objects.order_by("-pk").first()

        data = json.dumps(
            {
                "user_name": self.user_name,
                "ip_address": self.ip_address,
                "user_agent_string": self.user_agent_string,
                "timestamp": self.timestamp,
                "choices_provided": self.choices_provided,
                "choices_accepted": self.choices_accepted,
                "DJANGO_SECRET_KEY": settings.SECRET_KEY,
                "verification_hash_for_previous_entry": previous_log_entry.verification_hash
                if previous_log_entry
                else None,
            },
            sort_keys=True,
            cls=DjangoJSONEncoder
        )

        result = hashlib.md5(data.encode())

        self.verification_hash = result.hexdigest()

    def verify_hash(self):
        import hashlib
        import json
        from django.core.serializers.json import DjangoJSONEncoder

        if self.pk:
            previous_log_entry = (
                CookieConsentRecord.objects.filter(pk__lt=self.pk).order_by("-pk").first()
            )
        else:
            previous_log_entry = CookieConsentRecord.objects.order_by("-pk").first()

        data = json.dumps(
            {
                "user_name": self.user_name,
                "ip_address": self.ip_address,
                "user_agent_string": self.user_agent_string,
                "timestamp": self.timestamp,
                "choices_provided": self.choices_provided,
                "choices_accepted": self.choices_accepted,
                "DJANGO_SECRET_KEY": settings.SECRET_KEY,
                "verification_hash_for_previous_entry": previous_log_entry.verification_hash
                if previous_log_entry
                else None,
            },
            sort_keys=True,
            cls=DjangoJSONEncoder
        )

        result = hashlib.md5(data.encode())

        return self.verification_hash == result.hexdigest()
