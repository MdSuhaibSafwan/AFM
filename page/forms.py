from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row
from page.models import Page
from django import forms
from PIL import Image
from django.core.files.storage import default_storage as storage

class CreatePageForm(forms.ModelForm):
    STATUS_CHOICES = (
        (0, "Draft"),
        (1, "Publish"),
    )
    content = forms.CharField(label='Please enter your Page content (you can add text, links or images in your Page)', widget=CKEditorWidget())
    post_status = forms.ChoiceField(choices=STATUS_CHOICES,
                                    widget=forms.RadioSelect(attrs={'class': 'form-check-inline are_you_graduated',
                                                                    'required': True}))

    class Meta:
        model = Page
        fields = ['title', 'sub_title', 'content', 'parent', 'post_status']

        labels = {
            'title': 'Please enter the page title',
            'sub_title': 'Summary',
            'content': 'Please enter your page content (you can add text, links or images in your page)',
            'feature_image': 'Main image for your page (image dimension: 1800px width by 400px height)',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['content'].help_text = 'Write at least 500 words.'

    def clean(self):
        title = self.cleaned_data['title']
        if Page.objects.filter(title__iexact=title).exists():
            self.add_error('title', "Title is not unique")


class UpdateFeatureImageForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Page
        fields = ['feature_image', ]
        labels = {
            'feature_image': 'Main image for your page (Image dimension: 1800px width by 400px height)',
        }

    def save(self):
        post_image = super(UpdateFeatureImageForm, self).save()
        if self.cleaned_data.get('x') is not None:
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            image = Image.open(post_image.feature_image)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((500, 500), Image.ANTIALIAS)

            fh = storage.open(post_image.feature_image.name, "w")
            picture_format = 'png'
            resized_image.save(fh, picture_format)
            fh.close()
            return post_image