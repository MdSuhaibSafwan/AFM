from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row
from blogs.models import Post
from django import forms
from PIL import Image
from django.core.files.storage import default_storage as storage


class create_post_form(forms.ModelForm):
    STATUS_CHOICES = (
        (0, "Draft"),
        (1, "Submit for Review"),
    )
    content = forms.CharField(label='Please enter your blog content (you can add text, links or images in your blog)', widget=CKEditorWidget())
    post_status = forms.ChoiceField(choices=STATUS_CHOICES,
                                    widget=forms.RadioSelect(attrs={'class': 'form-check-inline are_you_graduated',
                                                                    'required': True}))

    class Meta:
        model = Post
        fields = ['title', 'sub_title', 'content', 'post_status']

        labels = {
            'title': 'Please enter the blog title',
            'sub_title': 'Summary',
            'content': 'Please enter your blog content (you can add text, links or images in your blog)',
            'feature_image': 'Main image for your blog (image dimension: 1800px width by 400px height)',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['content'].help_text = 'Write at least 500 words.'

    def clean(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title__iexact=title).exists():
            self.add_error('title', "Title is not unique")



class CreatPostForm(forms.ModelForm):
    STATUS_CHOICES = (
        (0, "Draft"),
        (1, "Submit for Review"),
    )
    post_status = forms.ChoiceField(choices=STATUS_CHOICES,
                                    widget=forms.RadioSelect(attrs={'class': 'form-check-inline'}),
                                    initial=1)
    content = forms.CharField(label='Please enter your blog content (you can add text, links or images in your blog)',
                              widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'sub_title', 'content', 'post_status']
        labels = {
            'title': 'Please enter the blog title',
            'sub_title': 'Summary',
            # 'feature_image': 'Main image for your blog (image dimension: 1800px width by 400px height)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['content'].help_text = 'Write at least 500 words.'


class EditPostForm(forms.ModelForm):
    content = forms.CharField(label='Please enter your blog content (you can add text, links or images in your blog)',
                              widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ['title', 'sub_title', 'content']
        labels = {
            'title': 'Please enter the blog title',
            'sub_title': 'Summary',
            # 'feature_image': 'Main image for your blog (image dimension: 1800px width by 400px height)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['content'].help_text = 'Write at least 500 words.'

class UpdateFeatureImageForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Post
        fields = ['feature_image', ]
        labels = {
            'feature_image': 'Main image for your blog (Image dimension: 1800px width by 400px height)',
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
            resized_image = cropped_image.resize((1800, 400), Image.ANTIALIAS)

            fh = storage.open(post_image.feature_image.name, "w")
            picture_format = 'png'
            resized_image.save(fh, picture_format)
            fh.close()
            return post_image