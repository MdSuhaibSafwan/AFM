from django import forms
from django.utils.translation import gettext_lazy as _


class CookieConsentSectionsForm(forms.Form):
    def __init__(self, request, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.controller = controller

        choices = [
            (section.slug, section.get_title())
            for section in controller.get_sections()
            if not section.is_required
        ]

        self.fields["sections"] = forms.MultipleChoiceField(
            required=False,
            label=_("Sections"),
            choices=choices,
            widget=forms.CheckboxSelectMultiple(),
        )
