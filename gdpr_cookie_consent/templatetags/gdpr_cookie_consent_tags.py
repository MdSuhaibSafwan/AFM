from django import template
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from django.conf import settings

from ..core import CookieConsentController

register = template.Library()


@register.simple_tag(takes_context=True)
def render_conditional_html(context):
    request = context["request"]
    controller = CookieConsentController(
        request=request, config=settings.COOKIE_CONSENT_SETTINGS
    )
    checked_sections = controller.checked_sections
    html_snippets = []
    for section in controller.get_sections():
        if section.slug in checked_sections:
            if not section.conditional_html_template_name:
                raise ImproperlyConfigured(
                    f"Section with slug {section.slug} doesn't have a conditional HTML template name."
                )
            context = {
                "cookie_consent_controller": controller,
                **controller.get_extra_context()
            }
            html_snippets.append(render_to_string(
                template_name=section.conditional_html_template_name,
                context=context,
                request=request,
            ))
    return mark_safe("\n".join(html_snippets))
