import json

from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .models import CookieConsentRecord


@admin.register(CookieConsentRecord)
class CookieConsentRecordAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "timestamp",
        "user_name",
        "ip_address",
        "user_agent_string",
        "get_choices_info",
        "continuity_verified",
    ]
    list_display_links = ["id", "timestamp"]
    list_filter = ["timestamp"]
    search_fields = ["user_name", "user_agent_string", "choices_accepted"]
    readonly_fields = ["timestamp", "continuity_verified"]
    fields = [
        "timestamp",
        "user",
        "user_name",
        "ip_address",
        "user_agent_string",
        "choices_provided",
        "choices_accepted",
        "continuity_verified",
    ]
    autocomplete_fields = ["user"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def continuity_verified(self, obj):
        return obj.verify_hash()

    continuity_verified.short_description = _("Record continuity verified")
    continuity_verified.boolean = True

    def get_choices_info(self, obj):
        sections = json.loads(obj.choices_json)
        return render_to_string("gdpr_cookie_consent/admin/choices_info.html", {"sections": sections})

    get_choices_info.short_description = _("Cookie Choices")
    get_choices_info.allow_tags = True
