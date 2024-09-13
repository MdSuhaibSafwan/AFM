def gdpr_cookie_consent(request):
    """
    Allows to access cookie consent controller from any template with request context, e.g.:

    {% if "functionality" in cookie_consent_controller.checked_sections %}
        <!-- add some optional functionality -->
    {% endif %}
    """
    from django.conf import settings
    from .core import CookieConsentController

    controller = CookieConsentController(
        request=request, config=settings.COOKIE_CONSENT_SETTINGS
    )
    return {
        "cookie_consent_controller": controller,
    }
