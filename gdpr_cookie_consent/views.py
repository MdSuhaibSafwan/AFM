import json

from django.shortcuts import render, redirect
from django.conf import settings
from django.http.response import JsonResponse, Http404
from django.db import transaction

from .core import CookieConsentController
from .forms import CookieConsentSectionsForm
from .models import CookieConsentRecord


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def cookies_management(request):
    data = {}
    controller = CookieConsentController(
        request=request, config=settings.COOKIE_CONSENT_SETTINGS
    )
    max_age = controller.get_consent_cookie_max_age()
    sections = [
        slug for slug in request.COOKIES.get("cookie_consent", "").split("|") if slug
    ]

    should_save = False
    if request.method == "POST":
        form = CookieConsentSectionsForm(
            request=request, controller=controller, data=request.POST
        )
        if form.is_valid():
            sections = form.cleaned_data["sections"]
            controller.update_checked_sections(sections)
            should_save = True
    else:
        form = CookieConsentSectionsForm(request=request, controller=controller)

    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        data["sections"] = sections
        if not form.is_valid():
            data["errors"] = form.errors.as_json()
        response = JsonResponse(data)
    elif should_save:
        response = redirect("/")
    else:
        context = {
            "form": form,
            "cookie_consent_controller": controller,
            **controller.get_extra_context(),
        }
        response = render(
            request, "gdpr_cookie_consent/cookies_management.html", context
        )

    if should_save:
        response.set_cookie(
            "cookie_consent",
            "|".join(sections),
            max_age=max_age,
            domain=settings.SESSION_COOKIE_DOMAIN,
        )
        for cookie in controller.get_cookies_to_delete():
            # Check if setting domain is mandatory
            response.delete_cookie(key=cookie.name, domain=cookie.domain)
        with transaction.atomic(using='afm'):
            record = CookieConsentRecord(
                user=request.user if request.user.is_authenticated else None,
                user_name=request.user.get_full_name()
                if request.user.is_authenticated
                else "Anonymous",
                ip_address=get_client_ip(request),
                user_agent_string=request.headers.get("User-Agent"),
                choices_provided=controller.get_human_readable_choices_provided(),
                choices_accepted=controller.get_human_readable_choices_accepted(),
                choices_json=json.dumps(controller.get_choices_dict()),
            )
            record.save()

    return response


def modal_dialog(request):
    controller = CookieConsentController(
        request=request, config=settings.COOKIE_CONSENT_SETTINGS
    )
    form = CookieConsentSectionsForm(request=request, controller=controller)

    context = {
        "form": form,
        "cookie_consent_controller": controller,
        **controller.get_extra_context(),
    }
    return render(request, "gdpr_cookie_consent/modal_dialog.html", context)


def conditional_html(request, slug):
    controller = CookieConsentController(
        request=request, config=settings.COOKIE_CONSENT_SETTINGS
    )
    section = controller.get_section(slug)
    if not section or not section.conditional_html_template_name:
        raise Http404("Sorry! Invalid section slug.")
    context = {
        "cookie_consent_controller": controller,
        **controller.get_extra_context(),
    }
    return render(
        request,
        section.conditional_html_template_name,
        context,
        content_type="text/plain",
    )
