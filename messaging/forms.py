from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div

from messaging.models import Messaging, ReportUser, PraiseUser, PraiseUserChoice


class MessagingForm(forms.ModelForm):
    class Meta:
        model = Messaging
        fields = ['comment']
        labels = {
            'comment': 'Add new comment'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5}, ),
        }


class ReportUserForm(forms.ModelForm):
    REASON_CHOICE = (
        # ('The User suggested communicating outside of TAG', 'The User suggested communicating outside of TAG'),
        ('The User behaved inappropriately', 'The User behaved inappropriately'),
        ('The User sent spam/other advertisements', 'The User sent spam/other advertisements'),
        ('Other', 'Other'),
    )
    reason_to_report = forms.ChoiceField(choices=REASON_CHOICE,
                                         widget=forms.RadioSelect(attrs={'required': 'required'}),
                                         required=True,
                                         label='Why do you wish to report this message?')

    class Meta:
        model = ReportUser
        fields = ['reason_to_report', 'message']
        labels = {
            'message': ''
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5,
                                             'placeholder': 'Please give further details on what went wrong'}, ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason_to_report'].help_text = 'This report will be kept anonymous'
        


class PraiseUserForm(forms.ModelForm):

    # reason_to_praise = forms.ModelMultipleChoiceField(queryset=PraiseUserChoice.objects.all(),
    #                                                        widget=forms.CheckboxSelectMultiple, required=True,
    #                                                        label="Praise this Mentor now!")

    class Meta:
        model = PraiseUser
        fields = ['message']
        labels = {
            'message': 'Message'
        }
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5,
                                             'placeholder': 'Please give further details of what you liked about this '
                                                            'mentor and why.'}, ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['reason_to_praise'].help_text = 'We may share your positive comments with this Mentor'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            # Row(
            #     Column('reason_to_praise', css_class='form-group col-sm-12 col-lg-12'),
            #     css_class='form-row'
            # ),
            Row(
                Column('message', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
        )
