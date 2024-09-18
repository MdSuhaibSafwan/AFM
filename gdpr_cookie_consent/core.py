from collections import namedtuple

from django.utils.translation import gettext
from django.utils.html import mark_safe
from django.template.loader import render_to_string


class ControllerBase(object):
    TEMPLATE_VARIABLE_NAME = "obj"

    def __init__(self, request, config, cookie_consent_controller):
        self.request = request
        self.config = config or {
            "description": "",
            "description_template_name": "",
        }
        self.cookie_consent_controller = cookie_consent_controller

    def __getattr__(self, item):
        return self.config.get(item)

    def get_description(self):
        description = self.config.get("description")
        description_template_name = self.config.get("description_template_name")
        if description:
            return mark_safe(f"<p>{gettext(description)}</p>")
        elif description_template_name:
            context = {
                self.TEMPLATE_VARIABLE_NAME: self,
                "cookie_consent_controller": self.cookie_consent_controller,
            }
            return render_to_string(
                template_name=description_template_name,
                context=context,
                request=self.request,
            )
        return ""


class CookieController(ControllerBase):
    TEMPLATE_VARIABLE_NAME = "cookie"

    def __init__(self, request, config, cookie_consent_controller):
        super().__init__(
            request=request,
            config=config,
            cookie_consent_controller=cookie_consent_controller,
        )

    def get_duration(self):
        duration = self.config.get("duration")
        if duration:
            return gettext(duration)
        return ""


class ProviderController(ControllerBase):
    TEMPLATE_VARIABLE_NAME = "provider"

    def __init__(self, request, config, cookie_consent_controller):
        super().__init__(
            request=request,
            config=config,
            cookie_consent_controller=cookie_consent_controller,
        )

    def get_title(self):
        title = self.config.get("title")
        if title:
            return gettext(title)
        return ""

    def get_cookies(self):
        for cookie_config in self.config.get("cookies", []):
            yield CookieController(
                request=self.request,
                config=cookie_config,
                cookie_consent_controller=self.cookie_consent_controller,
            )


class SectionController(ControllerBase):
    TEMPLATE_VARIABLE_NAME = "section"

    def __init__(self, request, config, cookie_consent_controller):
        super().__init__(
            request=request,
            config=config,
            cookie_consent_controller=cookie_consent_controller,
        )

    def get_title(self):
        title = self.config.get("title")
        if title:
            return gettext(title)
        return ""

    def get_summary(self):
        summary = self.config.get("summary")
        summary_template_name = self.config.get("summary_template_name")
        if summary:
            return mark_safe(f"<p>{gettext(summary)}</p>")
        elif summary_template_name:
            context = {
                self.TEMPLATE_VARIABLE_NAME: self,
                "cookie_consent_controller": self.cookie_consent_controller,
            }
            return render_to_string(
                template_name=summary_template_name,
                context=context,
                request=self.request,
            )
        return ""

    def get_providers(self):
        for provider_config in self.config.get("providers", []):
            yield ProviderController(
                request=self.request,
                config=provider_config,
                cookie_consent_controller=self,
            )

    def is_checked(self):
        slug = self.config.get("slug")
        return slug in self.cookie_consent_controller.checked_sections


Cookie = namedtuple("Cookie", "name domain")


class CookieConsentController(ControllerBase):
    TEMPLATE_VARIABLE_NAME = "controller"

    def __init__(self, request, config):
        super().__init__(request=request, config=config, cookie_consent_controller=self)
        self.checked_sections = [
            slug
            for slug in request.COOKIES.get("cookie_consent", "").split("|")
            if slug
        ]

    def update_checked_sections(self, sections):
        self.checked_sections = sections

    def get_base_template_name(self):
        return self.config.get("base_template_name", "base.html")

    def get_sections(self):
        for section_config in self.config.get("sections", []):
            yield SectionController(
                request=self.request,
                config=section_config,
                cookie_consent_controller=self,
            )

    def get_styling(self):
        return self.config.get("styling", {})

    def get_extra_context(self):
        return self.config.get("extra_context", {})

    def get_consent_cookie_max_age(self):
        six_months_approx = 60 * 60 * 24 * 30 * 6
        return self.config.get("consent_cookie_max_age", six_months_approx)

    def get_section(self, slug):
        for section in self.get_sections():
            if section.slug == slug:
                return section

    def get_extra_information(self):
        extra_information = self.config.get("extra_information")
        extra_information_template_name = self.config.get(
            "extra_information_template_name"
        )
        if extra_information:
            return mark_safe(f"<p>{gettext(extra_information)}</p>")
        elif extra_information_template_name:
            context = {
                self.TEMPLATE_VARIABLE_NAME: self,
                "cookie_consent_controller": self.cookie_consent_controller,
            }
            return render_to_string(
                template_name=extra_information_template_name,
                context=context,
                request=self.request,
            )
        return ""

    def get_cookies_to_delete(self):
        import fnmatch

        current_cookie_names = list(self.request.COOKIES.keys())
        cookies = []
        for section_controller in self.get_sections():
            if (
                not section_controller.required
                and section_controller.slug not in self.checked_sections
            ):
                for provider_controller in section_controller.get_providers():
                    for cookie_controller in provider_controller.get_cookies():
                        for cookie_name in fnmatch.filter(
                            current_cookie_names, cookie_controller.cookie_name
                        ):
                            cookies.append(
                                Cookie(
                                    cookie_name,
                                    cookie_controller.domain,
                                )
                            )
        return cookies

    def get_human_readable_choices_provided(self):
        lines = []
        for section in self.get_sections():
            lines.append(f"## {section.get_title()}\n")
            for provider in section.get_providers():
                lines.append(f"- {provider.get_title()}")
            lines.append("")
        return "\n".join(lines)

    def get_human_readable_choices_accepted(self):
        lines = []
        for section in self.get_sections():
            if section.required or section.slug in self.checked_sections:
                lines.append(f"## {section.get_title()}\n")
                for provider in section.get_providers():
                    lines.append(f"- {provider.get_title()}")
                lines.append("")
        return "\n".join(lines)

    def get_choices_dict(self):
        from collections import OrderedDict
        sections = OrderedDict()
        for section in self.get_sections():
            sections[section.slug] = {
                "slug": section.slug,
                "title": section.title,
                "required": section.required,
                "accepted": section.required or section.slug in self.checked_sections,
            }
        return sections

