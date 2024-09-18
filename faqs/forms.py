from django import forms
from faqs.models import Faq, FaqCategory
from administration.models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from ckeditor.widgets import CKEditorWidget

class FaqCategoryForm(forms.ModelForm):
    class Meta:
        model = FaqCategory
        exclude = ['created','updated']

class FaqForm(forms.ModelForm):
    description = forms.CharField(label='Please enter description here ',
                              widget=CKEditorWidget())
    class Meta:
        model = Faq
        fields = ['user_type', 'status', 'title', 'description', 'rank']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['rank'].help_text = 'Faqs will sort by this rank number in ascending order.'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('user_type', css_class='form-group col-md-4 mb-0'),
                Column('user_type', css_class='form-group col-md-4 mb-0'),
                Column('rank', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),

        )
