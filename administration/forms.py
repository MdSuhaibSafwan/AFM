from datetime import date
from decouple import config
from django import forms
from django.forms import CheckboxInput
from django_countries.fields import CountryField
from phonenumber_field.formfields import PhoneNumberField
from application.models import Application
from personal_information.models import CustomUserPersonalInformation, MentorPersonalInformation, \
    StudentPersonalInformation, TutoringSubject, TutoringWith, AppBasicInformation, \
    TutoringInLevel, SpokenLanguage, SkillsToDevelop, Hobby
from django.contrib.auth.forms import UserCreationForm
from administration.models import CustomUser, Institute, Mentor, Student, Parent, MentorFeedback, MentorBookingLeads, \
    InstituteScholarshipProgramme, BlockUser, ContactUs, MentorPublicProfileComment, TechSupport, Admin, \
    AdditionalQuestions, FutureStudent
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, Div, HTML, Field, Fieldset 
from crispy_forms.bootstrap import FieldWithButtons, StrictButton, AppendedText
# from captcha.fields import CaptchaField
from PIL import Image
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from AFM.widgets import ImageDropzoneWidget, FileDropzoneWidget, DropzoneWidget
from django.core.files.storage import default_storage as storage
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3
from .choices import questions_choice, platform_choice, how_did_you_hear_about_us_choices, SUBJECT, COURSE

LIST_OF_INSTITUTES = (
    ('', 'Select'),
    ('Barts & The London', 'Barts & The London'),
    ('Keele University', 'Keele University'),
    ('Canterbury Christ Church University', 'Canterbury Christ Church University'),
    ('University of Buckingham', 'University of Buckingham'),
    ('University of Aberdeen', 'University of Aberdeen'),
    ('International Foundation Group (IFG)', 'International Foundation Group (IFG)'),
    ('Abertay University', 'Abertay University'),
    ('University of the West of Scotland', 'University of the West of Scotland'),
    ('Aberystwyth University', 'Aberystwyth University'),
    ('Anglia Ruskin University', 'Anglia Ruskin University'),
    ('York St John University', 'York St John University'),
    ('Cardiff Metropolitan University', 'Cardiff Metropolitan University'),
    ('Arden University', 'Arden University'),
    ('Aston University Birmingham', 'Aston University Birmingham'),
    ('Wrexham Glyndŵr University', 'Wrexham Glyndŵr University'),
    ('Cardiff University', 'Cardiff University'),
    ('Bangor University', 'Bangor University'),
    ('Bath Spa University', 'Bath Spa University'),
    ('University of Worcester', 'University of Worcester'),
    ('Coventry University', 'Coventry University'),
    ('University of Wolverhampton', 'University of Wolverhampton'),
    ('University of Winchester', 'University of Winchester'),
    ('University of Westminster', 'University of Westminster'),
    ('Cranfield University', 'Cranfield University'),
    ('University of West London', 'University of West London'),
    ('Birmingham City University', 'Birmingham City University'),
    ('Bishop Grosseteste University', 'Bishop Grosseteste University'),
    ('De Montfort University', 'De Montfort University'),
    ('University of Warwick', 'University of Warwick'),
    ('Bournemouth University', 'Bournemouth University'),
    ('BPP University', 'BPP University'),
    ('Durham University', 'Durham University'),
    ('Brunel University', 'Brunel University'),
    ('University of Wales', 'University of Wales'),
    ('Bucks New University', 'Bucks New University'),
    ('University of the West of England', 'University of the West of England'),
    ('University of Ulster', 'University of Ulster'),
    ('University of East Anglia', 'University of East Anglia'),
    ('Edge Hill University', 'Edge Hill University'),
    ('Edinburgh Napier University', 'Edinburgh Napier University'),
    ('University of the Highlands & Islands', 'University of the Highlands & Islands'),
    ('University of the Arts London', 'University of the Arts London'),
    ('Falmouth University', 'Falmouth University'),
    ('University of Reading', 'University of Reading'),
    ('University of Sussex', 'University of Sussex'),
    ('Glasgow Caledonian University', 'Glasgow Caledonian University'),
    ('Harper Adams University', 'Harper Adams University'),
    ('University of Surrey', 'University of Surrey'),
    ('University of Sunderland', 'University of Sunderland'),
    ('Imperial College London', 'Imperial College London'),
    ('University of Suffolk', 'University of Suffolk'),
    ('University of Strathclyde', 'University of Strathclyde'),
    ('University of Stirling', 'University of Stirling'),
    ('Heriot-Watt University', 'Heriot-Watt University'),
    ('University of St Andrews', 'University of St Andrews'),
    ('University of Southampton', 'University of Southampton'),
    ('University of South Wales', 'University of South Wales'),
    ('Kingston University', 'Kingston University'),
    ('University of Sheffield', 'University of Sheffield'),
    ('Lancaster University', 'Lancaster University'),
    ('Leeds Beckett University', 'Leeds Beckett University'),
    ('University of Salford', 'University of Salford'),
    ('Leeds Trinity University', 'Leeds Trinity University'),
    ('University of Portsmouth', 'University of Portsmouth'),
    ('Liverpool Hope University', 'Liverpool Hope University'),
    ('University of Plymouth', 'University of Plymouth'),
    ('London Metropolitan University', 'London Metropolitan University'),
    ('Liverpool John Moores University', 'Liverpool John Moores University'),
    ('University of Oxford', 'University of Oxford'),
    ('University of Nottingham', 'University of Nottingham'),
    ('University of Northampton', 'University of Northampton'),
    ('King\'s College, London (KCL)', 'King\'s College, London (KCL)'),
    ('Hull York Medical School (HYMS)', 'Hull York Medical School (HYMS)'),
    ('University of Manchester', 'University of Manchester'),
    ('University of Glasgow', 'University of Glasgow'),
    ('University of Bradford', 'University of Bradford'),
    ('Middlesex University, London', 'Middlesex University, London'),
    ('Norwich University of the Arts', 'Norwich University of the Arts'),
    ('University of Dundee', 'University of Dundee'),
    ('University for the Creative Arts', 'University for the Creative Arts'),
    ('University of Central Lancashire', 'University of Central Lancashire'),
    ('Queen\'s University Belfast', 'Queen\'s University Belfast'),
    ('Royal Agricultural University', 'Royal Agricultural University'),
    ('Swansea University', 'Swansea University'),
    ('The Robert Gordon University, Aberdeen', 'The Robert Gordon University, Aberdeen'),
    ('University College, London (UCL)', 'University College, London (UCL)'),
    ('University of London', 'University of London'),
    ('University of Huddersfield', 'University of Huddersfield'),
    ('London South Bank University', 'London South Bank University'),
    ('University of Bolton', 'University of Bolton'),
    ('Newcastle University', 'Newcastle University'),
    ('University of Edinburgh', 'University of Edinburgh'),
    ('University of Derby', 'University of Derby'),
    ('Ravensbourne University London', 'Ravensbourne University London'),
    ('University of Cambridge', 'University of Cambridge'),
    ('Sheffield Hallam University', 'Sheffield Hallam University'),
    ('Teesside University, Middlesbrough and Darlington', 'Teesside University, Middlesbrough and Darlington'),
    ('St George\'s, University of London', 'St George\'s, University of London'),
    ('University of Liverpool', 'University of Liverpool'),
    ('University of Hertfordshire', 'University of Hertfordshire'),
    ('University of Exeter', 'University of Exeter'),
    ('University of Birmingham', 'University of Birmingham'),
    ('University of Essex', 'University of Essex'),
    ('Nottingham Trent University', 'Nottingham Trent University'),
    ('University of Cumbria', 'University of Cumbria'),
    ('University College Birmingham', 'University College Birmingham'),
    ('Queen Margaret University, Edinburgh', 'Queen Margaret University, Edinburgh'),
    ('Solent University', 'Solent University'),
    ('The Arts University Bournemouth', 'The Arts University Bournemouth'),
    ('St. Georges University, Grenada', 'St. Georges University, Grenada'),
    ('BSMS', 'BSMS'),
    ('University of Lincoln', 'University of Lincoln'),
    ('University of Greenwich', 'University of Greenwich'),
    ('Loughborough University', 'Loughborough University'),
    ('University of Bedfordshire, Luton and Bedford', 'University of Bedfordshire, Luton and Bedford'),
    ('Newman University, Birmingham', 'Newman University, Birmingham'),
    ('Oxford Brookes University', 'Oxford Brookes University'),
    ('University of Chichester', 'University of Chichester'),
    ('Regent\'s University London', 'Regent\'s University London'),
    ('University of Bristol', 'University of Bristol'),
    ('St Mary\'s University, Twickenham', 'St Mary\'s University, Twickenham'),
    ('The Open University', 'The Open University'),
    ('HYMS', 'HYMS'),
    ('University of Leicester', 'University of Leicester'),
    ('University of Leeds', 'University of Leeds'),
    ('University of Law', 'University of Law'),
    ('University of Gloucestershire', 'University of Gloucestershire'),
    ('University of Kent', 'University of Kent'),
    ('Manchester Metropolitan University', 'Manchester Metropolitan University'),
    ('University of Bath', 'University of Bath'),
    ('Northumbria University, Newcastle upon Tyne', 'Northumbria University, Newcastle upon Tyne'),
    ('University of East London', 'University of East London'),
    ('University of Chester', 'University of Chester'),
    ('Roehampton University, London', 'Roehampton University, London'),
    ('University of Brighton', 'University of Brighton'),
    ('Staffordshire University', 'Staffordshire University'),
    ('The Parkinson Building at the University of Leeds', 'The Parkinson Building at the University of Leeds'),
    ('European University Cyprus', 'European University Cyprus'),
    ('Other', 'Other'),
)

COURSES_LIST = (
    ('', 'Select'),
    (
    'University Foundation Programme in Business Management', 'University Foundation Programme in Business Management'),
    ('Foundation Programme in Engineering', 'Foundation Programme in Engineering'),
    ('Foundation Programme in Social Sciences', 'Foundation Programme in Social Sciences'),
    ('Foundation Programme in Computer Science', 'Foundation Programme in Computer Science'),
    ('Medical Foundation Programme', 'Medical Foundation Programme'),
    ('Diploma and Advanced Diploma in Business Management', 'Diploma and Advanced Diploma in Business Management'),
    ('Postgraduate Diploma in Business & Management', 'Postgraduate Diploma in Business & Management'),
    ('Undergraduate Level Courses', 'Undergraduate Level Courses'),
    ('Pre-Masters Programmes', 'Pre-Masters Programmes'),
    ('Pre-Doctoral Studies', 'Pre-Doctoral Studies'),
    ('English Language Programmes', 'English Language Programmes'),
    ('Pre-PhD Preparation Programme', 'Pre-PhD Preparation Programme'),
    ('Pre DBA Programme', 'Pre DBA Programme'),
)


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class MentorBookingLeadsForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = MentorBookingLeads
        fields = ['first_name', 'email', 'i_am',
                  'age_of_applicant', 'country', 'reasone_for_an_appointment', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3,
                                             'placeholder': 'Please be specific with your question(s). If you would '
                                                            'like to arrange a personal 1-to-1 video call with this '
                                                            'mentor,please state possible times and the time zone '
                                                            'where you are based.'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-sm-6 col-lg-6'),
                Column('i_am', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('age_of_applicant', css_class='form-group col-sm-6 col-lg-6'),
                Column('country', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('reasone_for_an_appointment', css_class='form-group col-sm-6 col-lg-6'),
                Column('email', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            'message',
            'captcha',
        )


class UpdateProfilePicForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta():
        model = CustomUser
        fields = ['profile_pic', ]
        labels = {
            'profile_pic': '',
        }

    def save(self):
        photo = super(UpdateProfilePicForm, self).save()
        if self.cleaned_data.get('x') is not None:
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')
            try:
                image = Image.open(photo.profile_pic)
                cropped_image = image.crop((x, y, w + x, h + y))
                resized_image = cropped_image.resize(
                    (128, 128), Image.ANTIALIAS)
                resized_image.save(photo.profile_pic.path)
            except:
                pass
        return photo


class RegistrationForm(UserCreationForm):
    # course = forms.ChoiceField(required=False, choices=COURSE)
    USER_TYPE_CHOICE = (
        # (3, 'Current IFG Student'),
        (12, 'Student'),
        (5, 'Parent'),
        )
    user_type = forms.ChoiceField(required=True, choices=USER_TYPE_CHOICE)
    # how_did_you_hear_about_us = forms.ChoiceField(required=True, choices=how_did_you_hear_about_us_choices,
    #                                               label='How did you hear about us?', )
    # how_did_you_hear_about_us_other = forms.CharField(
    #     required=False, max_length=30, label="Please provide specific details here*",
    #     widget=forms.TextInput(
    #         attrs={'class': 'form-control',
    #                'placeholder': 'Please be specific - include exact names, so we can thank them!'}))
    # captcha = ReCaptchaField(widget=ReCaptchaV3())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'user_type', 'email',
                  'password1', 'password2', ]
        labels = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'email': 'Email*',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'user_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'User Type', 'required': 'True'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'True'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.fields['course'].widget.attrs['disabled'] = False
        # self.fields['course'].initial = 'Medicine'
        self.fields['password1'].help_text = "Alphanumeric with min 8 characters"
        self.helper.layout = Layout(

            Row(
                Column('user_type', css_class='form-group col-sm-6 col-lg-6'),
                Column('email', css_class='form-group col-sm-6 col-lg-6'),
                # Column('how_did_you_hear_about_us', css_class='form-group col-sm-4 col-lg-4'),
                css_class='form-row'
            ),
            # Row(
            #     Column('how_did_you_hear_about_us_other', css_class='form-group col-sm-6 col-lg-6 how_did_you_hear_about_us_other'),
            #     css_class='form-row'
            # ),
            Row(
                Column('first_name', css_class='form-group col-sm-6 col-lg-6'),
                Column('last_name', css_class='form-group col-sm-6 col-lg-6'),
                # Column('course', css_class='form-group col-sm-4 col-lg-4'),
                css_class='form-row'
            ),

            Row(
                Column(
                    'password1', 
                    css_class='form-group col-sm-6 col-lg-6'
                ),
                Column(
                    'password2', 
                    css_class='form-group col-sm-6 col-lg-6'
                ),
            ),

            # Row(
            #     Column('password1', css_class='form-group col-sm-6 col-lg-6'),
            #     Column('password2', css_class='form-group col-sm-6 col-lg-6'),
            #     css_class='form-row'
            # ),
            Row(
                Column('captcha', css_class='form-group col-sm-6 col-lg-6 d-none'),
                css_class='form-row'
            ),
        )



class MentorRegistrationForm(UserCreationForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV3())
   
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'password1', 'password2']
        labels = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'email': 'Email*',
            'password1': "Password*",
            'password2': "Retype Password*",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("cc_myself")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['password1'].help_text = "Alphanumeric with min 8 characters"
        self.fields['password2'].help_text = "Retype the password again"
        self.helper.layout = Layout(
            
            Row(
                Column('first_name', css_class='form-group col-sm-6 col-lg-6'),
                Column('last_name', css_class='form-group col-sm-6 col-lg-6'),
                # Column('course', css_class='form-group col-sm-4 col-lg-4'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),

            Row(
                Column('password1', css_class='form-group col-sm-6 col-lg-6'),
                Column('password2', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            
            # Row(
            #     Column(
            #         AppendedText('password1', '<i data-feather="eye" class="eye-open toggle-password"></i>', active=True), 
            #         css_class='form-group col-sm-6 col-lg-6'
            #     ),
            #     Column(
            #         AppendedText('password2', '<i data-feather="eye" class="eye-open toggle-password"></i>', active=True), 
            #         css_class='form-group col-sm-6 col-lg-6'
            #     ),
            # ),
            
            # Row(
            #     Column('password1', css_class='form-group col-sm-6 col-lg-6'),
            #     Column('password2', css_class='form-group col-sm-6 col-lg-6'),
            #     css_class='form-row'
            # ),
            
            # Row(
            #     Column(
            #         Field('password1', template="conditional_html/eye-password1.html"),
            #     css_class='form-group col-sm-12 col-lg-6'
            #     ),
            #     Column(
            #         Field('password2', template="conditional_html/eye-password2.html"),
            #     css_class='form-group col-sm-12 col-lg-6'
            #     ),          
            #     css_class='form-row'
            # ),

            Row(
                Column('captcha', css_class='form-group col-sm-6 col-lg-6 d-none'),
                css_class='form-row'
            ),
        )




class IFGStudentRegistrationForm(UserCreationForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV3())
   
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'password1', 'password2']
        labels = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'email': 'Email*',
            'password1': "Password*",
            'password2': "Retype Password*",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@intfoundationgroup.co.uk', 'required': 'True'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['password1'].help_text = "Alphanumeric with min 8 characters"
        self.fields['password2'].help_text = "Retype the password again"
        self.helper.layout = Layout(
            
            Row(
                Column('first_name', css_class='form-group col-sm-6 col-lg-6'),
                Column('last_name', css_class='form-group col-sm-6 col-lg-6'),
                # Column('course', css_class='form-group col-sm-4 col-lg-4'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),

            Row(
                Column('password1', css_class='form-group col-sm-6 col-lg-6'),
                Column('password2', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            
            # Row(
            #     Column(
            #         AppendedText('password1', '<i data-feather="eye" class="eye-open toggle-password"></i>', active=True), 
            #         css_class='form-group col-sm-6 col-lg-6'
            #     ),
            #     Column(
            #         AppendedText('password2', '<i data-feather="eye" class="eye-open toggle-password"></i>', active=True), 
            #         css_class='form-group col-sm-6 col-lg-6'
            #     ),
            # ),
            
            Row(
                Column('captcha', css_class='form-group col-sm-6 col-lg-6 d-none'),
                css_class='form-row'
            ),

        )



class ChatRegistrationForm(UserCreationForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV3())

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'password1', 'password2']
        labels = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'email': 'Email*',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'True'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email already exists !!")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['password1'].help_text = "Alphanumeric with min 8 characters"
        self.helper.layout = Layout(
            HTML('<h6>Register using Email</h6>'),
            Row(
                Column('email', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            
            Row(
                Column('first_name', css_class='form-group col-sm-6 col-lg-6'),
                Column('last_name', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'password1', 
                    css_class='form-group col-sm-6 col-lg-6'
                ),
                Column(
                    'password2', 
                    css_class='form-group col-sm-6 col-lg-6'
                ),
            ),
        )





class AppAdminRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email


class InstituteRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', ]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email


class InstituteScholarshipForm(forms.ModelForm):
    class Meta:
        model = Institute
        fields = ['institute_name', 'country', 'funding_last_year', 'funding_current_year',
                  'countries_available', 'extra_notes']
        labels = {
            'funding_last_year': 'Funding Last Year(GBP)',
            'funding_current_year': 'Funding Current Year(GBP)',
        }
        widgets = {
            'extra_notes': forms.Textarea(attrs={'rows': 2}),
        }



class CustomUserPersonalInformationForm(forms.ModelForm):
    spoken_languages = forms.ModelMultipleChoiceField(queryset=SpokenLanguage.objects.all(),required=True)
    hobbies = forms.ModelMultipleChoiceField(queryset=Hobby.objects.all(),required=True,label='Hobbies and Interests')
    class Meta:
        model = CustomUserPersonalInformation
        fields = ('first_name', 'last_name', 'gender', 'currently_living_in',
                  'country', 'spoken_languages', 'date_of_birth', 'about_me', 'hobbies', 'phone')
        widgets = {
            # 'date_of_birth': forms.TextInput(attrs={'class': 'form-control', 'required': 'True'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter firstname(s)', 'required': 'True'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter lastname', 'required': 'True'}),
            'gender': forms.Select(attrs={'class': 'select form-control'}),
            'spoken_languages': forms.Select(attrs={'class': 'select form-control'}),
            'hobbies': forms.Select(attrs={'class': 'select form-control'}),
            'currently_living_in': forms.Select(attrs={'class': 'select form-control'}),
            'about_me': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please do not include any contact information here..',
                       'rows': 3, 'required': True, 'minlength': 250}, ),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth',
            'spoken_languages': 'Spoken Languages',
            'country': 'Please select country were you hold a passport',
            'phone': 'Your Cell/Mobile Number',
            'about_me': 'About Me*',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kept_private_fields = ['last_name', 'gender', 'phone']
        # for field in kept_private_fields:
        #     self.fields[field].label += "<span class='text-danger'> († Kept private)</span>"
        for field in kept_private_fields:
            self.fields[field].required = False
        self.fields['spoken_languages'].help_text = 'Please select at least one. You may select ' \
                                                    'more than one language.'
        self.fields['phone'].help_text = 'We may add this number to our internal WhatsApp account for ' \
                                         'verification and efficient communication purposes.'
        self.fields['about_me'].help_text = 'Please provide information about you here. Include your future goals, ' \
                                            'ambitions.<br>' \
                                            'You can also include any experience you have helping other students ' \
                                            'here too. The more useful information you add, the more popular your ' \
                                            'profile will be.' \
                                            '<br>Please <strong>do not</strong> include any personal or contact ' \
                                            'information here.'
        # self.fields['phone'].widget.attrs['pattern'] = '[0-9]'
        # self.fields['phone'].widget.attrs['title'] = 'Please include numbers only'
        # self.fields['phone'].help_text = 'Please include country dialling code. eg: for UK +44125552368'

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (dob.year + 15, dob.month, dob.day) > (today.year, today.month, today.day):
            raise forms.ValidationError(
                'Must be at least 15 years old to register')
        return dob


class ProfilePhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    rotation = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    profile_pic = forms.FileField(widget=forms.FileInput(attrs={'accept': 'image/jpg'}))

    class Meta:
        model = CustomUserPersonalInformation
        fields = ('profile_pic',)
        # widgets = {
        #     'profile_pic': DropzoneWidget,
        # }
        labels = {
            'profile_pic': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    def save(self):
        photo = super(ProfilePhotoForm, self).save()
        if self.cleaned_data.get('x') is not None:
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')

            image = Image.open(photo.profile_pic)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((300, 300), Image.LANCZOS)

            fh = storage.open(photo.profile_pic.name, "wb")
            picture_format = 'png'
            resized_image.save(fh, picture_format)
            fh.close()
            return photo




NEW_SUBJECT_LIST = [
    ('', 'Select'), 
    (11, 'Architecture'), 
    (3, 'Arts & Design'), 
    (5, 'Biomedical Sciences'), 
    (1, 'Business Studies'), 
    (15, 'Chemical Engineering'), 
    (20, 'Civil Engineering'), 
    (9, 'Computer Science'), 
    (7, 'Dentistry'), 
    (19, 'Economics'), 
    (16, 'Electrical Engineering'), 
    (10, 'Finance'), 
    (12, 'Finance & Accounting'), 
    (17, 'International Relations'), 
    (4, 'Law'), 
    (18, 'Mechanical Engineering'), 
    (6, 'Medicine'), 
    (13, 'Nursing'), 
    (8, 'Pharmacy'), 
    (14, 'Politics'), 
    (2, 'Social Studies'),
    (21, 'Other'),
    ]


class MentorUpdateInformationFirstStepForm(forms.ModelForm):
    
    currently_studying = forms.ChoiceField(choices=NEW_SUBJECT_LIST,
                                                 label='Subject field you are currently studying')

    class Meta:
        model = MentorPersonalInformation
        fields = ['currently_studying','university_email','studying_in',]

        labels = {
            'university_email': 'Your University email',
            'studying_in': 'Country studying In',
            'currently_studying': 'Subject field you are currently studying',
            # 'phone': 'Your Phone Number',
            # 'passport': 'Upload photo of your student ID card',
        }

        widgets = {
            'studying_in': forms.Select(attrs={'class': 'select form-control'}),
            'currently_studying': forms.Select(attrs={'class': 'select form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # kept_private_fields = ['passport']
        # for field in kept_private_fields:
        #     self.fields[field].label += "<span class='text-danger'> († Kept private)</span>"
        # self.fields['currently_studying_dummy'].widget.attrs['disabled'] = True
        # self.fields['phone'].widget.attrs['pattern'] = '^\+(?:[0-9]●?){6,14}[0-9]$'
        # self.fields['phone'].widget.attrs['title'] = 'Please include country dialling code. eg: for UK +44125552368'
        # self.fields['phone'].help_text = 'Please include country dialling code. eg: for UK +44125552368'
        self.fields['currently_studying'].help_text = 'Eg: Law, Engineering'


class MentorUpdateInformationSecondStepForm(forms.ModelForm):
    are_you_graduated = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(
        attrs={'class': 'form-check-inline are_you_graduated'}),
                                          label='Are you currently a university student?')
    are_you_registered_as_an_ambassador = forms.ChoiceField(choices=questions_choice,
                                                            widget=forms.RadioSelect(attrs={'required': 'required'}),
                                                            required=True,
                                                            label="Are you registered as an Ambassador for your "
                                                                  "existing university?")

    # did_you_study_the_foundation_course_in_uk = forms.ChoiceField(choices=questions_choice, widget=forms.Select(
    #     attrs={'class': 'select form-control foundation-in'}), required=True,
    #                                                               label="Did you study a foundation/pathway course?")
    # dbs_check = forms.ChoiceField(choices=questions_choice,
    #                               widget=forms.RadioSelect(attrs={'required': 'required'}),
    #                               label='Have you had a recent DBS checked?')
    # WHERE_DID_YOU_STUDY_CHOICES = (
    #     ('On the same campus as my current university',
    #      'On the same campus as my current university'),
    #     ('Other', 'Other'),
    # )
    # where_did_you_study = forms.ChoiceField(choices=WHERE_DID_YOU_STUDY_CHOICES,
    #                                         label='Where did you study this foundation/pathway course?*',
    #                                         required=False)
    # experience_in_content_creation = forms.ChoiceField(choices=questions_choice,
    #                                                    widget=forms.RadioSelect(attrs={'required': 'required'}),
    #                                                    label='Do you have experience in writing website/blog content?')
    # profile_made_visible_to_employers = forms.ChoiceField(choices=questions_choice,
    #                                                       widget=forms.RadioSelect(attrs={'required': 'required'}),
    #                                                       label='Would you like potential employers to show interest '
    #                                                             'in your profile? ie: Employers would see your '
    #                                                             'academic background, skills and achievements but not '
    #                                                             'identity you personally. You can then decide at a '
    #                                                             'later date if you wish to pass on any further '
    #                                                             'details to them if their approach is of interest to '
    #                                                             'you.',
    #                                                       )
    # bool_choice = (
    #     (False, 'NO'),
    #     (True, 'YES'),
    # )
    # are_you_a_uk_national = forms.ChoiceField(choices=bool_choice, widget=forms.RadioSelect(),
    #                                           label='Is your nationality UK?', )
    # tier_4_visa_allow_you_to_work_in_uk = forms.ChoiceField(choices=bool_choice, widget=forms.RadioSelect(),
    #                                                         label='Does your Tier 4 Student Visa allow you to be '
    #                                                               'employed in the UK?')
    # eligible_to_work_in_country_living_in = forms.ChoiceField(choices=bool_choice,
    #                                                           widget=forms.RadioSelect(attrs={'required': 'required'}),
    #                                                           label='Are you eligible to work in country you are '
    #                                                                 'living in?')
    # skills_to_develop = forms.ModelMultipleChoiceField(queryset=SkillsToDevelop.objects.all(),
    #                                                     widget=forms.CheckboxSelectMultiple, required=False,
    #                                                     label="What core skills are you hoping to develop?*")
    #
    # would_you_like_us_to_generate_a_CV = forms.ChoiceField(choices=questions_choice,
    #                                                        widget=forms.RadioSelect(),
    #                                                        label='Would you like us to generate a CV template for you '\
    #                                                                 'based on the information you have provided?')

    class Meta:
        model = MentorPersonalInformation
        fields = [
            # 'did_you_study_the_foundation_course_in_uk',
            # 'where_did_you_study',
            # 'foundation_provider',
            'university_start_year',
            # 'year_graduated',
            'previous_qualification',
            'name_of_school', 'are_you_graduated',
            'are_you_registered_as_an_ambassador',
            # 'linkedin_profile_url', 'facebook_profile_url', 'instagram_profile_url', 'tiktok_profile_url',
            # 'twitter_profile_url',
            # 'follow_us_on_facebook', 'follow_us_on_tiktok',
            # 'follow_us_on_instagram', 'follow_us_on_twitter',
            # 'follow_us_on_linkedin', 'follow_us_on_youtube',
            # 'about_content_creation', 'experience_in_content_creation',
            # 'profile_made_visible_to_employers', 'about_yourself',
            # 'preferred_career_field', 'preferred_location', 'skills_to_develop',
            # 'where_will_you_be_during_the_completion_of_your_internship', 'duration_of_internship',
            # 'weekly_working_hours',
            # 'cv',
            # 'would_you_like_us_to_generate_a_CV',
            # 'dbs_check', 'dbs_Reference_no', 'dbs_date', 'dbs_certificate_no',
            # 'dbs_declaration',
            # 'are_you_a_uk_national', 'tier_4_visa_allow_you_to_work_in_uk', 'visa_start_date',
            # 'visa_end_date', 'brp_card',
            # 'eligible_to_work_in_country_living_in'
        ]

        labels = {
            # 'foundation_provider': 'What was the name of this course/foundation/pathway provider?*',
            'year': 'Year*',
            # 'study_year': 'What year are you studying on your current course?*',
            'university_start_year': 'What year did you leave IFG?',
            # 'year_graduated': 'Year Graduated*',
            'student_id': 'Student ID',
            'name_of_school': 'Please enter the name of the school where you studied before starting at IFG',
            'are_you_registered_as_an_ambassador': 'Are you registered as an Ambassador for your existing university?',
            # 'tutoring_subject': 'I can tutor you with',
            # 'tutoring_with': 'I can help you with',
            # 'write_something_about_you': 'Write something about you',
            # 'tutor_exp': 'Tutoring Experience',
            # 'facebook_profile_url': '<i data-feather="facebook"></i> Facebook profile',
            # 'instagram_profile_url': '<i data-feather="instagram"></i> Instagram profile',
            # 'tiktok_profile_url': '<i data-feather="video"></i> TikTok profile',
            # 'twitter_profile_url': '<i data-feather="twitter"></i> Twitter profile',
            # 'linkedin_profile_url': '<i data-feather="linkedin"></i> LinkedIn profile',
            # 'follow_us_on_facebook': '<i data-feather="facebook"></i> <a href="https://www.facebook.com/ApplyForMedicine" target="blank">Facebook</a>',
            # 'follow_us_on_instagram': '<i data-feather="instagram"></i> <a href="https://www.instagram.com/applyformedicine/" target="blank">Instagram</a>',
            # 'follow_us_on_tiktok': '<i data-feather="video"></i> <a href="https://www.tiktok.com/@tagtheapplygroup" target="blank">TikTok</a>',
            # 'follow_us_on_twitter': '<i data-feather="twitter"></i> <a href="https://twitter.com/ApplyforMed" target="blank">Twitter</a>',
            # 'follow_us_on_linkedin': '<i data-feather="linkedin"></i> <a href="https://www.linkedin.com/company/theapplygroup/" target="blank">LinkedIn</a>',
            # 'follow_us_on_youtube': '<i data-feather="youtube"></i> <a href="https://www.youtube.com/channel/UCXCV7gYPrQTPRf2dyZJrNuQ" target="blank">Youtube</a>',
            # 'about_content_creation': 'Please provide details',
            # 'about_yourself': 'Please write a few words about yourself here*',
            # 'preferred_career_field': 'Preferred Career Field*',
            # 'preferred_location': 'Preferred Location*',
            # 'where_will_you_be_during_the_completion_of_your_internship': 'Where Will You be During the Completion of Your Internship Program?*',
            # 'duration_of_internship': 'Duration*',
            # 'weekly_working_hours': 'Max number of hours you could commit per week*',
            # 'cv': 'Upload your CV',
            # 'dbs_check': 'Have you had a DBS or Police check in the last 12 months?',
            # 'dbs_certificate_type': 'DBS Certificate Type',
            # 'dbs_Reference_no': 'DBS ID number',
            # 'dbs_date': 'Date of issue',
            # 'dbs_certificate_no': 'Certificate number',
            # 'dbs_certificate': 'Upload a scanned copy of your DBS certificate',
            # 'tutoring_subject_other': 'Tutoring Subject',
            # 'tutoring_in_level': 'Subject Level',
            'previous_qualification': 'Please state the course you studied at IFG and the grade you achieved',
            # 'brp_card': 'Please upload a scanned copy/image of your <a href="https://www.gov.uk/biometric-residence-permits" target="blank">BRP (Biometric Residence Permits)</a> card',

        }

        widgets = {
            # 'did_you_study_the_foundation_course_in_uk': forms.Select(
            #     attrs={'class': 'select form-control foundation-in'}),
            # 'subject': forms.Select(attrs={'class': 'select form-control'}),
            'programme_level': forms.Select(attrs={'class': 'select form-control'}),
            # 'study_year': forms.Select(attrs={'class': 'select form-control'}),
            # 'year_graduated': forms.Select(attrs={'class': 'select form-control'}),
            'university_start_year': forms.Select(attrs={'class': 'select form-control'}),
            'name_of_school': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your secondary/highschool name'}),
            'are_you_registered_as_an_ambassador': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
            # 'facebook_profile_url': forms.TextInput(
            #     attrs={'class': 'form-control', 'placeholder': 'Please add your Facebook URL here'}),
            # 'instagram_profile_url': forms.TextInput(
            #     attrs={'class': 'form-control', 'placeholder': 'Please add your Instagram URL here'}),
            # 'tiktok_profile_url': forms.TextInput(
            #     attrs={'class': 'form-control', 'placeholder': 'Please add your TikTok URL here'}),
            # 'twitter_profile_url': forms.TextInput(
            #     attrs={'class': 'form-control', 'placeholder': 'Please add your Twitter URL here'}),
            # 'linkedin_profile_url': forms.TextInput(
            #     attrs={'class': 'form-control', 'placeholder': 'Please add your LinkedIn URL here'}),
            'are_you_graduated': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
            # 'experience_in_content_creation': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
            # 'about_content_creation': forms.Textarea(
            #     attrs={'class': 'form-control',
            #            'placeholder': 'Eg: blogs, vlogs, articals etc add links to your work if possible', 'rows': 3}),
            # 'about_yourself': forms.Textarea(
            #     attrs={'class': 'form-control',
            #            'placeholder': 'eg. Why have you chosen this specific field. You long term interests and goals.'\
            #                           ' Your personality and any other achievements.',
            #            'rows': 6}),
            'previous_qualification': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'You may also include other qualifications you have ...',
                       'rows': 3}),

            # # 'phone': PhoneNumberPrefixWidget(attrs={'class': 'form-control textInput form-control phone_number'}),
            # 'dbs_declaration': forms.Textarea(
            #     attrs={'class': 'form-control',
            #            'placeholder': 'eg: Any convictions, etc.',
            #            'rows': 3}),
            # 'follow_us_on_facebook': CheckboxInput(),
            # 'follow_us_on_instagram': CheckboxInput(),
            # 'follow_us_on_tiktok': CheckboxInput(),
            # 'follow_us_on_twitter': CheckboxInput(),
            # 'follow_us_on_linkedin': CheckboxInput(),
            # 'follow_us_on_youtube': CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        kept_private_fields = ['are_you_graduated', 'university_start_year',
                               # 'did_you_study_the_foundation_course_in_uk',
                               'name_of_school',
                               # 'where_did_you_study'
                               ]
        for field in kept_private_fields:
            self.fields[field].required = False
        # for field in kept_private_fields:
        #     self.fields[field].label += "<span class='text-danger'> († Kept private)</span>"
        # self.fields['phone'].widget.attrs['pattern'] = '^\+(?:[0-9]●?){6,14}[0-9]$'
        # self.fields['phone'].widget.attrs['title'] = 'Please include country dialling code. eg: for UK +44125552368'
        # self.fields['phone'].help_text = 'Please include country dialling code. eg: for UK +44125552368'
        # self.fields['currently_studying'].help_text = 'Eg: Law, Engineering'
        self.fields[
            'previous_qualification'].help_text = 'Eg: I got 74% on Medical Foundation Programme and an average of 7.5 bands in IELTS.'
        # self.fields['dbs_Reference_no'].widget.attrs['oninput'] = 'javascript: if (this.value.length > ' \
        #                                                           'this.maxLength) this.value = this.value.slice(0, ' \
        #                                                           'this.maxLength); '
        # self.fields['dbs_certificate_no'].widget.attrs['oninput'] = 'javascript: if (this.value.length > ' \
        #                                                             'this.maxLength) this.value = this.value.slice(0, ' \
        #                                                             'this.maxLength); '
        # self.fields['dbs_certificate_no'].widget.attrs['title'] = 'Maximum 12 digits.'
        # self.fields['dbs_certificate_no'].widget.attrs['maxLength'] = 12
        #
        # self.fields['dbs_Reference_no'].widget.attrs['title'] = 'Maximum 12 digits.'
        # self.fields['dbs_Reference_no'].widget.attrs['maxLength'] = 12



class StudentQuestionForm(forms.ModelForm):
    institute_list = forms.ChoiceField(required=False, choices=LIST_OF_INSTITUTES,
                                       label="Your Selected Institute")
    # captcha = ReCaptchaField(widget=ReCaptchaV3())
    institute_name = forms.CharField(
        required=False, max_length=30, label="University Name*")

    class Meta:
        model = Student
        fields = ['q1', 'q2', 'q3', 'q4']
        widgets = {
            'q1': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: what to focus on, practice speaking English, mix with other students, new experiences', 'rows': 3}),
            'q2': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: more about university options, life abroad , how to connect with current IFG students', 'rows': 3}),
            'q3': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: Learning to focus during tutorials, asking questions, focussing on certain modules', 'rows': 3}),
            'q4': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: new skills and knowledge, busy, exciting, social life, costs, safety, etc', 'rows': 3}),
            'q5': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: I found accommodation by....., I paid £xxx a week for food, etc', 'rows': 3}),
        }
        labels = {
            'q1': 'What advice would you give to a future student?',
            'q2': 'What do you wish you had known before you started your IFG Course?',
            'q3': 'What important skills do you think you have developed so far at IFG?',
            'q4': 'Please summarise your experience studying at IFG?',
            'q5': 'Please give information on the cost of living/accommodation while studying at IFG?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['q1'].required = False
        self.fields['q2'].required = False
        self.fields['q3'].required = False
        self.fields['q4'].required = False
        self.fields['q5'].required = False
        
        


class StudentProfileStep1Form(forms.ModelForm):
    class Meta:
        model = StudentPersonalInformation
        fields = ['area_of_study','student_id_card','institute_email']

        widgets = {
            'area_of_study': forms.Select(attrs={'class': 'select form-control'}),
            # 'subject_foundation': forms.Select(attrs={'class': 'select form-control'}),
            # 'study_destination': forms.Select(attrs={'class': 'select form-control'})
        }

        labels = {
            # 'subject_foundation': 'IFG Course',
            'area_of_study': 'Course you are currently studying',  
            'student_id_card': 'Upload photo of your student ID card', 
            'institute_email': 'Your IFG email',
            # 'study_destination': 'Country where studying IFG Course'
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.fields['student_id_card'].required = False
            self.fields['institute_email'].required = False
            

class StudentPersonalInformationFirstStepForm(forms.ModelForm):
    class Meta:
        model = StudentPersonalInformation

        fields = [
            'area_of_study', 'programme_level',
            'level_of_english',
            ]

        widgets = {
            'area_of_study': forms.Select(attrs={'class': 'select form-control'}),
            'programme_level': forms.Select(attrs={'class': 'select form-control'}),
            'level_of_english': forms.Select(attrs={'class': 'select form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        

class StudentConsentForm(forms.ModelForm):
    class Meta:
        model = StudentPersonalInformation
        fields = ['media_consent','consent1']
                  
        labels = {
            # 'media_consent': "I consent for the above information to be used internally for administrative purpose "
            #             "and some information to be made public on my public profile.",
            'media_consent': "I give permission for this photograph, or other data that I may submit, will be used on my profile "
                        "and for other promotional purposes for the IFG, including their website homepage.", 
            'consent1': "I consent that my personal data will be used in accordance to the <a "
                        "href='" + config('AFM_LINK') + "/privacy-notice' target='_blank'>Privacy Notice.</a> "
                       
        }
        widgets = {
            'media_consent': CheckboxInput(attrs={'required': 'required'}),
            'consent1': CheckboxInput(attrs={'required': 'required'}),
        }



class ApplicantAdditionalQuestionsForm(forms.ModelForm):
    class Meta:
        model = AdditionalQuestions
        fields = ['q1']
        widgets = {
            'q1': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Write your question here...', 'rows': 1, }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Row(
                Column('q1', css_class='form-group col-sm-12 col-md-12 col-lg-12 mb-0'),
                css_class='form-row'
            ),
            'id',
        )


class MentorConsentForm(forms.ModelForm):
    class Meta:
        model = MentorPersonalInformation
        fields = ['consent1', 'consent2',
                  'consent3', 'consent4']
        labels = {
            'consent1': "I agree to the <a href='" + config(
                'AFM_LINK') + "/terms-and-conditions' target='_blank'>Terms & "
                              "Conditions</a>.",
            'consent2': "I agree to the mentor <a href='" + config(
                'AFM_LINK') + "/codes-of-conduct' target='_blank'>Codes "
                              "of Conduct</a>.",
            'consent3': "I consent that my personal data will be used in accordance to the <a "
                        "href='" + config('AFM_LINK') + "/privacy-notice' target='_blank'>Privacy Notice.</a> ",
            'consent4': "I give permission for this photograph, or other data that I may submit, will be used on my profile "
                        "and for other promotional purposes for the IFG, including their website homepage.",
        }
        widgets = {
            'consent1': CheckboxInput(attrs={'required': 'required'}),
            'consent2': CheckboxInput(attrs={'required': 'required'}),
            'consent3': CheckboxInput(attrs={'required': 'required'}),
            'consent4': CheckboxInput(attrs={'required': 'required'}),
        }


class update_user_info(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'First Name*',
            'last_name': 'Last Name*',
            'email': 'Email Address',
        }
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter firstname(s)', 'required': 'True'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter lastname', 'required': 'True'}),
            'email': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter lastname', 'required': 'True',
                       'readonly': 'True'}),

        }


class parent_form(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['phone_no', 'address', 'city', 'state', 'postcode', 'country']
        widgets = {

            'address': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, }),

            'city': forms.TextInput(
                attrs={'class': 'form-control', }),
            'state': forms.TextInput(
                attrs={'class': 'form-control', }),
            'postcode': forms.TextInput(
                attrs={'class': 'form-control', }),

            'country': forms.Select(attrs={'class': 'select form-control'}),
            # 'phone_no': PhoneNumberPrefixWidget(
            #     attrs={'class': 'form-control textinput textInput form-control phone_number'}),

        }
        labels = {
            'postcode': 'Pincode/Zipcode/Postal Code',
            'phone_no': 'Your Phone Number',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.fields['phone_no'].widget.attrs['pattern'] = '^\+(?:[0-9]●?){6,14}[0-9]$'
        # self.fields['phone_no'].widget.attrs['title'] = 'Please include country dialling code. eg: for UK +44125552368'
        # self.fields['phone_no'].help_text = 'Please include country dialling code. eg: for UK +44125552368'


class MentorProfileForm(forms.ModelForm):
    institute_list = forms.ChoiceField(required=False, choices=LIST_OF_INSTITUTES,
                                       label="Your Selected Institute")
    # captcha = ReCaptchaField(widget=ReCaptchaV3())
    institute_name = forms.CharField(
        required=False, max_length=30, label="University Name*")

    class Meta:
        model = Mentor
        fields = ['institute_list', 'institute_name', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7']
        widgets = {
            # 'institute': forms.Select(attrs={'class': 'select form-control'}),
            'q1': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: what to focus on, practice speaking English, mix with other students, new experiences', 'rows': 3}),
            'q2': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: more about university options, life abroad , how to connect with current IFG students', 'rows': 3}),
            'q3': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: social life, accommodation options,  clubs/societies, number of students, travel', 'rows': 3}),
            'q4': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: Learning to focus during tutorials, asking questions, focussing on certain modules', 'rows': 3}),
            'q5': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: new skills and knowledge, busy, exciting, social life, costs, safety, etc', 'rows': 3}),
            'q6': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'The UCAS process, getting offers, making choices, CAS, student visa', 'rows': 3}),
            'q7': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Eg: I found accommodation by....., I paid £xxx a week for food, etc', 'rows': 3}),
        }
        
        labels = {
            'institute_name': 'Institute name*',
            'institute': 'Select Institute*',
            'q1': 'What advice would you give to a future student?',
            'q2': 'What do you wish you had known before you started your IFG Course?',
            'q3': 'What do you wish you had known about your current university before you started? ',
            'q4': 'What important  skills did you develop while at IFG?',
            'q5': 'Please summarise your experience studying at IFG and living in London/Abu Dhabi ?',
            'q6': 'What top tips to can you provide to apply to university?',
            'q7': 'Please give information on the cost of living/accommodation when studying at IFG?',            
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        question_list = ['q1','q2','q3','q4','q5','q6','q7']
        for q in question_list:
            self.fields[q].required=False

        # self.fields[
        #     'q1'].help_text = 'Eg: Study hard on certain modules, practice speaking English, mix with other students'
        # self.fields[
        #     'q2'].help_text = 'Eg: I should have applied sooner, prepared for IELTS earlier, connected with students already there'
        # self.fields[
        #     'q3'].help_text = 'Eg: Learning to focus during tutorials, asking questions, focussing on certain modules'
        # self.fields['q4'].help_text = 'Eg: Busy, exciting, many activities, high-costs, safety, etc'
        # self.fields['q5'].help_text = 'Eg: Apply early, improve English language skills by....'
        # self.fields['q6'].help_text = 'Eg: I found accommodation by....., I paid £xxx a week for food, etc'


class MentorPersonalInformationForm(forms.ModelForm):
    are_you_graduated = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(
        attrs={'class': 'form-check-inline are_you_graduated'}),
                                          label='Are you currently a university student?')
    are_you_registered_as_an_ambassador = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                                            required=True,
                                                            label="Are you registered as an Ambassador for your "
                                                                  "existing university?")
    are_you_currently_a_tutor = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(), required=True,
                                                  label='Are you currently a tutor?')
    did_you_study_the_foundation_course_in_uk = forms.ChoiceField(choices=questions_choice, widget=forms.Select(
        attrs={'class': 'select form-control foundation-in'}), required=True,
                                                                  label="Did you study a foundation/pathway course?")
    dbs_check = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                  label='Have you had a recent DBS checked?')
    WHERE_DID_YOU_STUDY_CHOICES = (
        ('On the same campus as my current university',
         'On the same campus as my current university'),
        ('Other', 'Other'),
    )
    where_did_you_study = forms.ChoiceField(choices=WHERE_DID_YOU_STUDY_CHOICES,
                                            label='Where did you study this foundation/pathway course?*',
                                            required=False)
    experience_in_content_creation = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                                       label='Do you have experience in writing website/blog content?')
    profile_made_visible_to_employers = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                                          label='Would you like potential employers to show interest '
                                                                'in your profile? ie: Employers would see your '
                                                                'academic background, skills and achievements but not '
                                                                'identify you personally. You can then decide at a '
                                                                'later date if you wish to pass on any further '
                                                                'details to them if their approach is of interest to '
                                                                'you.',
                                                          )
    TUTORING_SUBJECT_CHOICES = (
        ("Maths", "Maths"),
        ("Physics", "Physics"),
        ("Chemistry", "Chemistry"),
        ("English", "English"),
        ("Economics", "Economics"),
        ("ICT", "ICT"),
        ("History", "History"),
        ("Geography", "Geography"),
        ("Personal Statement", "Personal Statement"),
        ("Interviews", "Interviews"),
    )

    TUTORING_WITH = (
        ("UCAT", "UCAT"),
        ("BMAT", "BMAT"),
        ("GAMSAT", "GAMSAT"),
        ("HPAT", "HPAT"),
        ("IMAT", "IMAT"),
        ("Personal Statement", "Personal Statement"),
        ("MMI / Interviews", "MMI / Interviews"),

    )
    TUTORING_LEVEL = (
        ('Highschool', 'Highschool'),
        ('College / University', 'College / University'),
        ('English Language', 'English Language'),
    )
    tutoring_subject_list = forms.ModelMultipleChoiceField(queryset=TutoringSubject.objects.all(),
                                                           widget=forms.CheckboxSelectMultiple, required=False,
                                                           label="Tutoring subject(s)")

    tutoring_with_list = forms.ModelMultipleChoiceField(queryset=TutoringWith.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple, required=False,
                                                        label="Tutoring with")

    tutoring_in_level_list = forms.ModelMultipleChoiceField(queryset=TutoringInLevel.objects.all(),
                                                            widget=forms.CheckboxSelectMultiple, required=False,
                                                            label="Tutoring level(s)")
    bool_choice = (
        (False, 'NO'),
        (True, 'YES'),
    )
    are_you_a_uk_national = forms.ChoiceField(choices=bool_choice, widget=forms.RadioSelect(),
                                              label='Is your nationality UK?', )
    tier_4_visa_allow_you_to_work_in_uk = forms.ChoiceField(choices=bool_choice, widget=forms.RadioSelect(),
                                                            label='Does your Tier 4 Student Visa allow you to be employed in the UK?')
    eligible_to_work_in_country_living_in = forms.ChoiceField(choices=bool_choice, widget=forms.RadioSelect(),
                                                              label='Are you eligible to work in country you are living in?')

    class Meta:
        model = MentorPersonalInformation
        fields = ['studying_in', 'passport', 'did_you_study_the_foundation_course_in_uk',
                  'where_did_you_study', 'year_graduated', 'study_year',
                  'previous_qualification',
                  'name_of_school',
                  'are_you_registered_as_an_ambassador',
                  'are_you_currently_a_tutor',
                  'do_you_tutor_privately_or_online', 'online_platform', 'tutoring_subject_list',
                  'tutoring_subject_other',
                  'tutoring_with_list',
                  'tutoring_in_level_list', 'currently_studying',
                  'linkedin_profile_url', 'are_you_graduated',
                  'about_content_creation', 'experience_in_content_creation',
                  'profile_made_visible_to_employers', 'about_yourself',
                  'dbs_check', 'dbs_Reference_no', 'dbs_date', 'dbs_certificate_no',
                  'dbs_declaration',
                  'are_you_a_uk_national', 'tier_4_visa_allow_you_to_work_in_uk', 'visa_start_date', 'visa_end_date',
                  'foundation_provider', 'eligible_to_work_in_country_living_in', 'consent1', 'consent2']
        labels = {
            'studying_in': 'Country studying In',
            'currently_studying': 'What subject field are you currently studying?',
            'passport': 'Upload photo of your student ID card',
            'where_did_you_study': 'Please select where did you study?*',
            'subject_foundation': 'Subject Foundation*',
            'foundation_provider': 'What was the name of this course/foundation/pathway provider?*',
            'year': 'Year*',
            'study_year': 'What year are you studying on your current course?*',
            'year_graduated': 'Year Graduated*',
            'student_id': 'Student ID',
            'name_of_school': 'Please enter the name of the school where you studied before starting at your current '
                              'university',
            'are_you_registered_as_an_ambassador': 'Are you registered as an Ambassador for your existing university?',
            'are_you_currently_a_tutor': 'Are you currently a tutor?',
            'do_you_tutor_privately_or_online': 'Do you tutor privately or with any tutoring agency/online platform?',
            'online_platform': 'Please enter their name here',
            'tutoring_subject': 'I can tutor you with',
            'tutoring_with': 'I can help you with',
            'write_something_about_you': 'Write something about you',
            'tutor_exp': 'Tutoring Experience',
            'linkedin_profile_url': 'Please add your LinkedIn profile URL here',
            'about_content_creation': 'Please provide details',
            'about_yourself': 'Please write a few words about yourself here*',
            'dbs_check': 'Have you had a DBS or Police check in the last 12 months?',
            'dbs_certificate_type': 'DBS Certificate Type',
            'dbs_Reference_no': 'DBS ID number',
            'dbs_date': 'Date of issue',
            'dbs_certificate_no': 'Certificate number',
            'dbs_certificate': 'Upload a scanned copy of your DBS certificate',
            'tutoring_subject_other': 'Tutoring Subject',
            'tutoring_in_level': 'Subject Level',
            'previous_qualification': 'Any other qualification you would like to add?',
            'consent1': "I agree to the <a href='" + config(
                'AFM_LINK') + "/terms-and-conditions' target='_blank'>Terms & "
                              "Conditions</a> and confirm that above "
                              "information is true to the best of my knowledge and agree to the <a "
                              "href='" + config('AFM_LINK') + "/codes-of-conduct' "
                                                              "target='_blank'>Mentor Codes of Conduct</a>",
            'consent2': "I consent for the above information to be used internally and some information made visible "
                        "publicly on my Mentor profile page as shown on <a "
                        "href='" + config('AFM_LINK') + "/mentor-profile1/' target='_blank'>sample profile</a> "
                                                        "here.",

        }

        widgets = {
            'studying_in': forms.Select(attrs={'class': 'select form-control'}),
            'did_you_study_the_foundation_course_in_uk': forms.Select(
                attrs={'class': 'select form-control foundation-in'}),
            'subject': forms.Select(attrs={'class': 'select form-control'}),
            'programme_level': forms.Select(attrs={'class': 'select form-control'}),
            'study_year': forms.Select(attrs={'class': 'select form-control'}),
            'year_graduated': forms.Select(attrs={'class': 'select form-control'}),
            'name_of_school': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Your secondary/highschool name'}),
            'are_you_registered_as_an_ambassador': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
            'are_you_currently_a_tutor': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
            'currently_studying': forms.Select(attrs={'class': 'select form-control'}),
            'write_something_about_you': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please describe why you would be best suited to mentor/tutor prospective '
                                      'university applicants. (Use this section to promote your skills such as any '
                                      'clubs or societies you belong to, your hobbies and interest etc.)',
                       'rows': 3}),
            'linkedin_profile_url': forms.URLInput(
                attrs={'class': 'form-control', 'placeholder': 'Please add your LinkedIn URL here'}),
            'are_you_graduated': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
            'experience_in_content_creation': forms.RadioSelect(attrs={'class': 'form-check-inline'}),
            'about_content_creation': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Eg: blogs, vlogs, articles etc add links to your work if possible', 'rows': 3}),
            'about_yourself': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please highlight your career interests, relevant experience and predicted degree score',
                       'rows': 4}),
            'previous_qualification': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Write about previous qualifications...', 'rows': 3}),
            # 'phone': PhoneNumberPrefixWidget(attrs={'class': 'form-control textInput form-control phone_number'}),
            'dbs_declaration': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'eg: Any convictions, etc.',
                       'rows': 3}),
            'consent1': CheckboxInput(),
            'consent2': CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        kept_private_fields = ['passport', 'are_you_graduated', 'study_year',
                               'did_you_study_the_foundation_course_in_uk', 'name_of_school', 'where_did_you_study']
        for field in kept_private_fields:
            self.fields[field].label += "<span class='text-danger'> († Kept private)</span>"
        # self.fields['phone'].widget.attrs['pattern'] = '^\+(?:[0-9]●?){6,14}[0-9]$'
        # self.fields['phone'].widget.attrs['title'] = 'Please include country dialling code. eg: for UK +44125552368'
        # self.fields['phone'].help_text = 'Please include country dialling code. eg: for UK +44125552368'
        self.fields['currently_studying'].help_text = 'Eg: Law, Engineering'
        self.fields['previous_qualification'].help_text = 'Eg: any advisory, mentoring or counselling courses'

        self.fields['dbs_Reference_no'].widget.attrs['oninput'] = 'javascript: if (this.value.length > ' \
                                                                  'this.maxLength) this.value = this.value.slice(0, ' \
                                                                  'this.maxLength); '
        self.fields['dbs_certificate_no'].widget.attrs['oninput'] = 'javascript: if (this.value.length > ' \
                                                                    'this.maxLength) this.value = this.value.slice(0, ' \
                                                                    'this.maxLength); '
        self.fields['dbs_certificate_no'].widget.attrs['title'] = 'Maximum 12 digits.'
        self.fields['dbs_certificate_no'].widget.attrs['maxLength'] = 12

        self.fields['dbs_Reference_no'].widget.attrs['title'] = 'Maximum 12 digits.'
        self.fields['dbs_Reference_no'].widget.attrs['maxLength'] = 12


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['id', 'admin', 'mentor']
        widgets = {
            'profile_pic': forms.FileInput(attrs={'class': 'form-control afm-user-img'}),
        }


class StudentPersonalInformationForm(forms.ModelForm):
    LAST_QUALIFICATION = (
        ('Highschool', 'Highschool'),
        ('Post 16 Secondary', 'Post 16 Secondary'),
        ('College', 'College'),
        ('Undergraduate Degree', 'Undergraduate Degree'),
    )
    last_qualification = forms.ChoiceField(choices=LAST_QUALIFICATION,
                                           label='What is your most recent qualification?*', required=False)

    what_are_you_studying = forms.ChoiceField(choices=LAST_QUALIFICATION,
                                              label='At what level are you currently studying?*', required=False)

    class Meta:
        model = StudentPersonalInformation
        # exclude = ['id', 'admin', 'about_me']
        fields = ['level_of_english', 'currently_studying', 'current_or_last_school_name', 'what_are_you_studying',
                  'last_qualification',
                  'study_destination', 'area_of_study', 'programme_level', 'intake_year', 'consent1']
        labels = {
            'area_of_study': 'Subject Interest',
            'programme_level': 'Desired Programme Level',
            'what_are_you_studying': 'At what level are you currently studying?*',
            'currently_studying': 'Are you currently studying?',
            'current_or_last_school_name': 'School Name*',
            'study_destination': 'Desired Study Destination(s)',
            'intake_year': 'Which year would you like to start?',
            'level_of_english': 'What is your level of English?',
            'consent1': "I have read and agree to the student <a href='" + config('AFM_LINK') + "/codes-of-conduct' "
                                                                                                "target='_blank'> Student/Applicant Codes of Conduct</a> and "
                                                                                                "<a href='" + config(
                'AFM_LINK') + "/online-safety' target='_blank'>Online Safety Policy.</a>"
        }
        widgets = {
            'level_of_english': forms.Select(attrs={'class': 'form-control'}),
            'currently_studying': forms.Select(attrs={'class': 'form-control'}),
            'intake_year': forms.Select(attrs={'class': 'select form-control'}),
            'what_are_you_studying': forms.TextInput(attrs={'class': 'form-control'}),
            'last_qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'programme_level': forms.Select(attrs={'class': 'select form-control'}),
            'about_me': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'consent1': CheckboxInput(attrs={'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['area_of_study'].widget.attrs['readonly'] = True
        self.fields['area_of_study'].widget.attrs['style'] = "pointer-events:none;"
        self.fields['study_destination'].help_text = "*Please note that if you are not considering applying for " \
                                                     "universities outside the EU, you will be able to book " \
                                                     "appointments for Mentoring and Tutoring purposes only. "


class InstituteAdminRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email


class SystemMentorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email


class SystemRecruiterRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email


class InstituteUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()

    def clean_email(self):
        username = self.cleaned_data.get("username")
        email = self.cleaned_data.get("email")
        print('username', username)
        print('email', email)
        if CustomUser.objects.filter(username=email).exclude(username=username).exists():
            raise forms.ValidationError("Email is not unique")
        return email


class LatepointLinkForm(forms.ModelForm):
    class Meta:
        model = MentorPersonalInformation
        fields = ['late_point', ]

        labels = {
            'late_point': 'Add meeting link here'
        }


class RecruiterRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    email = forms.EmailField(required=True)
    WORK_TYPE_CHOICE = (
        (1, 'Company'),
        (2, 'Individual'),
        (3, 'School'),
    )
    work_type = forms.ChoiceField(required=True, choices=WORK_TYPE_CHOICE)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'work_type',
                  'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email

    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name(s)'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        'work_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'User Type', 'required': 'True'}),
        'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'True'}),
        'password1': forms.PasswordInput(
            attrs={'class': 'form-control', ' placeholder': 'Password', 'required': 'True'}),
        'password2': forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Re-type Password', 'required': 'True'}),

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('work_type', css_class='form-group col-sm-6 col-lg-6'),
                Column('email', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-sm-6 col-lg-6'),
                Column('last_name', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-sm-6 col-lg-6'),
                Column('password2', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),

        )


class SchoolRegistrationForm(UserCreationForm):
    school_name = forms.CharField(required=True)
    website = forms.URLField(required=True, max_length=200, )
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['school_name', 'website',
                  'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email

    widgets = {
        'school_name': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'School Name', 'required': 'True'}),
        'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'True'}),
        'password1': forms.PasswordInput(
            attrs={'class': 'form-control', ' placeholder': 'Password', 'required': 'True'}),
        'password2': forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Re-type Password', 'required': 'True'}),

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('school_name', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-sm-6 col-lg-6'),
                Column('website', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-sm-6 col-lg-6'),
                Column('password2', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
        )


class BlockUserForm(forms.ModelForm):
    class Meta:
        model = BlockUser
        fields = ['message', 'is_removed']

        labels = {
            'message': 'Please write your complain here'
        }


class ContactUsForm(forms.ModelForm):
    # captcha = CaptchaField()
    captcha = ReCaptchaField(widget=ReCaptchaV3())

    class Meta:
        model = ContactUs
        fields = ['name', 'country', 'i_am_a', 'email',
                  'phone_no', 'subject', 'message', 'captcha']
        labels = {
            'message': 'Your Message',
            'name': 'Your Name'
        }
        widgets = {
            'phone_no': PhoneNumberPrefixWidget(attrs={'class': 'form-control textInput phone_number'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('name', css_class='form-group col-sm-12 col-lg-6'),
                Column('country', css_class='form-group col-sm-12 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('i_am_a', css_class='form-group col-sm-6 col-lg-6'),
                Column('email', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'phone_no', css_class='form-group col-sm-6 col-lg-6 phone_field'),
                Column('subject', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('message', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column(Field('captcha', css_class='form-control'),
                       css_class='form-group col-sm-6 col-lg-6 d-none'),
                css_class='form-row'
            ),

        )


class TechSupportForm(forms.ModelForm):
    class Meta:
        model = TechSupport
        fields = ['subject', 'message']
        labels = {
            'message': '',
            'subject': '',
        }
        widgets = {
            'message': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Your Message',
                       'rows': 3})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['subject'].widget.attrs['placeholder'] = "Subject"
        self.helper.layout = Layout(
            Field('subject', css_class='form-control'),
            Field('message', css_class='form-control'),
        )


class MessageMentorForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3())
    i_am_a_choose = (
        (1, 'Student'),
        (2, 'Parent'),
    )
    i_am_a = forms.ChoiceField(required=True, choices=i_am_a_choose)
    question1 = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(), required=True,
                                  label='Would you like to book an appointment with this mentor?')

    class Meta:
        model = ContactUs
        fields = ['name', 'country', 'i_am_a', 'email', 'phone_no',
                  'subject', 'question1', 'message', 'captcha']
        labels = {
            'message': 'Your Message',
            'name': 'Your Name',
            'country': 'Country you reside in',
        }
        widgets = {
            'phone_no': PhoneNumberPrefixWidget(attrs={'class': 'form-control textInput phone_number'}),
            'message': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please state what specific assistance you would like from this mentor '
                                      'and your preferred times & dates (in your local time) for your '
                                      'appointment.',
                       'rows': 5})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('question1', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('name', css_class='form-group col-sm-12 col-lg-6'),
                Column('country', css_class='form-group col-sm-12 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('i_am_a', css_class='form-group col-sm-6 col-lg-6'),
                Column('email', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'phone_no', css_class='form-group col-sm-6 col-lg-6 phone_field'),
                Column('subject', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('message', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column(Field('captcha', css_class='form-control'),
                       css_class='form-group col-sm-6 col-lg-6 d-none'),
                css_class='form-row'
            ),

        )


class UniversityContactUsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3())

    class Meta:
        model = ContactUs
        fields = ['i_am_a', 'connect_with_a_mentor', 'email',
                  'phone_no', 'subject', 'message', 'captcha']
        labels = {
            'message': 'Your Message'
        }
        widgets = {
            'phone_no': PhoneNumberPrefixWidget(attrs={'class': 'form-control textInput phone_number'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('connect_with_a_mentor',
                       css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('i_am_a', css_class='form-group col-sm-12 col-lg-12'),

                css_class='form-row'
            ),
            Row(

                Column('email', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'phone_no', css_class='form-group col-sm-12 col-lg-12 phone_field'),
                Column('subject', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('message', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column(Field('captcha', css_class='form-control d-none'),
                       css_class='form-group col-sm-12 col-lg-12'),

                css_class='form-row'
            ),
        )


class MentorPublicProfileCommentForm(forms.ModelForm):
    class Meta:
        model = MentorPublicProfileComment
        fields = ['comment']
        labels = {
            'comment': 'Add new comment'
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5}, ),
        }


class AdminMeetingLinkForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = ['meeting_link', 'appointment_link']


class MentorUpdateAboutFieldForm(forms.ModelForm):
    class Meta:
        model = CustomUserPersonalInformation
        fields = ['about_me']

        widgets = {
            'about_me': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please describe why you would be best suited to mentor/tutor prospective '
                                      'university applicants.(Use this section to promote your skills such as any '
                                      'clubs or societies you belong to, your hobbies and interest etc.)',
                       'rows': 10, 'required': True, 'minlength': 250}, ),
        }


class MentorUpdateYoutubeShotsFieldForm(forms.ModelForm):
    youtube_shots = forms.URLField(required=True, label='Add Youtube Shots Link')

    class Meta:
        model = MentorPersonalInformation
        fields = ['youtube_shots']


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    USER_TYPE_CHOICE = (
        ('', 'Select user'),
        (1, 'Admin'),
        (3, 'Current Student'),
        (4, 'Former Student'),
        (5, 'Parent'),
    )
    user_type = forms.ChoiceField(required=True, choices=USER_TYPE_CHOICE)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'user_type', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Email is not unique")
        return email


class StudentQuestionsAboutSchool(forms.ModelForm):
    are_you_studying_an_online_course = forms.ChoiceField(choices=questions_choice,
                                                          widget=forms.RadioSelect(attrs={'required': 'required'}),
                                                          required=True,
                                                          label='Are you studying an <strong>online</strong> IFG '
                                                                'Course/Programme?')

    currently_studying_course = forms.ChoiceField(required=True, choices=COURSES_LIST)

    class Meta:
        model = Student
        fields = ['q1', 'q2', 'q3', 'q4',
                  'are_you_studying_an_online_course',
                  'currently_studying_course'
                  ]
        labels = {
            'q1': '<strong>What advice would you give to future students?</strong>',
            'q2': '<strong>What do you most like about studying at IFG?</strong>',
            'q3': '<strong>How does IFG help you to progress your goals?</strong>',
            'q4': '<strong>Any other information you would like to share?</strong>',
            'currently_studying_course': 'Currently Studying (IFG programmes)',
        }
        widgets = {
            'q1': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please write your answer here..',
                       'rows': 2, 'required': True, }, ),
            'q2': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please write your answer here..',
                       'rows': 2, 'required': True, }, ),
            'q3': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please write your answer here..',
                       'rows': 2, 'required': True, }, ),
            'q4': forms.Textarea(
                attrs={'class': 'form-control',
                       'placeholder': 'Please write your answer here..',
                       'rows': 2, 'required': True, }, ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['q1'].help_text = "Eg: Student life, teaching and making the most of their time at IFG., etc"
        self.fields['q2'].help_text = "Eg: Teaching,  expert guidance, etc"
        self.fields['q3'].help_text = "Eg: University progression, improve English, etc"
        self.fields['q4'].help_text = "Eg: Accommodation, Student support, activities, etc"
        self.helper.layout = Layout(
            Row(
                Column('q1', css_class='form-group col-sm-6 col-lg-6'),
                Column('q2', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('q3', css_class='form-group col-sm-6 col-lg-6'),
                Column('q4', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
        )


class StudentAdditionalPersonalInformation(forms.ModelForm):
    class Meta:
        model = AppBasicInformation
        fields = ['native_languages', 'currently_living_in', ]
        labels = {
            'native_languages': 'Native Languages',
        }


class FutureStudentInformation(forms.ModelForm):

    PROGRAM_LEVEL_CHOICES = (
        ('Undergraduate', 'Undergraduate'),
        ('Postgraduate', 'Postgraduate'),
    )
    program_level = forms.ChoiceField(choices=PROGRAM_LEVEL_CHOICES, widget=forms.RadioSelect(),
                                      required=True,
                                      label='Are you considering undergraduate or postgraduate course?')
    course_you_interested_in = forms.ChoiceField(required=True, choices=COURSES_LIST,
                                                 label='What course/programme are you interested in?')
                                                 
    have_you_already_applied_to_this_school = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                                                required=True,
                                                                label='Have you already applied to International '
                                                                      'Foundation Group (IFG)?')

    class Meta:
        model = FutureStudent
        fields = ['have_you_already_applied_to_this_school', 'where_are_you_from', 'intake_year', 'intake_month',
                  'course_you_interested_in', 'program_level']
        labels = {
            'where_are_you_from': 'Which country are you from?',
            'intake_year': 'Possible start year',
            'intake_month': 'Possible start month',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('have_you_already_applied_to_this_school', css_class='form-group col-sm-6 col-lg-6'),
                Column('program_level', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('where_are_you_from', css_class='form-group col-sm-6 col-lg-6'),
                Column('course_you_interested_in', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('intake_year', css_class='form-group col-sm-6 col-lg-6'),
                Column('intake_month', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(

            ),
        )



class FutureStudentSignupForm(forms.ModelForm):
    PROGRAM_LEVEL_CHOICES = (
        ('Undergraduate', 'Undergraduate'),
        ('Postgraduate', 'Postgraduate'),
        ('Research', 'Research')
    )
    program_level = forms.ChoiceField(choices=PROGRAM_LEVEL_CHOICES, widget=forms.RadioSelect(),
                                      required=True,
                                      label='Are you considering undergraduate or postgraduate course?')
    course_you_interested_in = forms.ChoiceField(required=True, choices=COURSES_LIST,
                                                 label='What course/programme are you interested in?')
                                                 
    have_you_already_applied_to_this_school = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                                                required=True,
                                                                label='Applied to International '
                                                                      'Foundation Group (IFG) before?')
    class Meta:
        model = FutureStudent
        fields = ['have_you_already_applied_to_this_school', 'where_are_you_from', 'intake_year', 'intake_month',
                  'course_you_interested_in', 'program_level']
        labels = {
            'where_are_you_from': 'Nationality',
            'intake_year': 'Possible start year',
            'intake_month': 'Possible start month',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            
            Row(
                Column('where_are_you_from', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('have_you_already_applied_to_this_school', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('intake_year', css_class='form-group col-sm-6 col-lg-6'),
                Column('intake_month', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('program_level', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('course_you_interested_in', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            
        )