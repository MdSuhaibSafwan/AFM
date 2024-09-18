import html
from django import forms
from datetime import date
from administration.context_processors import current_user
from administration.templatetags.administration_extras import getifneedtheartical
from application.models import Application, AcademicQualification, EnglishLanguage, Reference, \
    PersonalStatement, VisaHistory, ApplicationOfferStatus, ApplicationComment, ProfessionalExperience, \
    ProfessionalTrainingCertificate, DirectApplication, ConsideredApplication, DocumentUpload, \
    FinalSelected, ApplicationFeedback
from administration.models import Institute, Mentor, Student, Parent
from personal_information.models import MentorPersonalInformation, AppBasicInformation, AppAddress, \
    AppPassportInformation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML
from AFM.utils import get_current_request
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from administration.templatetags.administration_extras import getsubject
from django.templatetags.static import static

questions_choice = (
    (0, 'NO'),
    (1, 'YES'),
)


class DateInput(forms.DateInput):
    input_type = "date"


class CustomMCF(forms.ModelChoiceField):
    def label_from_instance(self, user):
        print(user.admin.slug)
        user_mentor_pi = MentorPersonalInformation.objects.get(admin__user_slug=user.admin.slug)

        return "%s: Studying %s in %s <img src='%s' >" % (user_mentor_pi.admin.first_name,
                                                          getsubject(user_mentor_pi.currently_studying),
                                                          user_mentor_pi.studying_in.name,
                                                          user_mentor_pi.admin.profile_pic.url if user_mentor_pi.admin.profile_pic else static(
                                                              'images/default_profile.png')
                                                          )


class SelectMentorForm(forms.ModelForm):
    active_mentors = MentorPersonalInformation.objects.using(
        'afm_personal_information').filter(currently_studying=6).values('admin__user_slug')
    temp = []
    # for i in active_mentors:
        # temp.append(i['admin__user_slug'])
    queryset = Mentor.objects.filter(profile_status=True, admin__is_active=True, admin__slug__in=temp)
    mentor = CustomMCF(queryset=queryset,
                       label='If a Mentor helped you to complete your application form, please select them here',
                       required=False)

    class Meta:
        model = Application
        fields = ['mentor']


class ApplicationForm(forms.ModelForm):
    about_me = forms.CharField(widget=forms.Textarea(attrs={'rows': 5,
                                                            'placeholder': 'Please do not include any personal or '
                                                                           'contact information here.'
                                                            }),
                               label="About me"
                               )

    class Meta:
        model = AppBasicInformation
        fields = ['about_me',
                  # 'subject', 'program_level', 'intake_month', 'intake_year', 'desire_course', 'fees_affordability',
                  # 'scholarship_option', 'exclude_institutes', 'exclude_institutes_other', 'study_destination_country',
                  # 'level_of_english'
                  ]

        labels = {
            # 'subject': 'Subject Interest',
            # 'program_level': 'Desired Programme Level',
            # 'intake_month': 'Desired Intake Month',
            # 'intake_year': 'Desired Intake Year',
            # 'desire_course': 'Desired Course (if known)',
            # 'selected_institutes': 'Selected Institutes',
            # 'fees_affordability': 'What is your tuition fee budget per academic year? (in GBP)',
            # 'scholarship_option': 'Would you like to be considered for a scholarship? (if available)',
            # 'study_destination_country': 'Study Destination(s)',
            # 'exclude_institutes': 'Are there any institutions that you do not wish to apply to? (optional)',
            # 'exclude_institutes_other': 'Are there any institutions that you do not wish to apply to? (optional)',
            'about_me': 'About Applicant',
            # 'level_of_english': 'What is your level of English?',

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.fields[
        #     'exclude_institutes'].help_text = "Eg. Because you may have applied to them previously for this intake."
        # self.fields[
        #     'exclude_institutes_other'].help_text = "Eg. Because you may have applied to them previously for this intake."
        # self.fields['intake_month'].help_text = "Please select the nearest month"
        self.fields['about_me'].help_text = 'Please write about your ' \
                                           'interests, hobbies, achievements and what '\
                                           'sort of courses you are interested in '\
                                           'studying. The more details and information '\
                                           'you can provide the more useful this tool '\
                                           'will be for you. Ideal points to include are: your ambition, future goals.'\
                                           '<br>Please <strong>do not</strong> include any personal or contact ' \
                                           'information here.'
        # self.fields[
        #     'fees_affordability'].help_text = "<span>You can view the current exchange rate on : <a " \
        #                                       "href='https://xe.com/' target='_blank'>xe.com</a> "
        # self.fields['desire_course'].widget.attrs['placeholder'] = 'Do you have any specific course preference?'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            # Row(
            #     Column('subject', css_class='form-group col-md-4 mb-0'),
            #     Column('program_level', css_class='form-group col-md-4 mb-0'),
            #     Column('desire_course', css_class='form-group col-md-4 mb-0'),
            #     css_class='row my-form'
            # ),
            # Row(
            #     Column('intake_month', css_class='form-group col-md-4 mb-0'),
            #     Column('intake_year', css_class='form-group col-md-4 mb-0'),
            #     Column('study_destination_country', css_class='form-group col-md-4 mb-0'),
            #     css_class='form-row'
            # ),
            # Row(
            #     Column('fees_affordability', css_class='form-group col-md-6 mb-0'),
            #     Column('scholarship_option', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            # Row(
            #     Column('level_of_english', css_class='form-group col-md-4 mb-0'),
            #     Column('exclude_institutes', css_class='form-group col-md-8 mb-0'),
            #     Column('exclude_institutes_other', css_class='form-group col-md-8 mb-0'),
            #     css_class='form-row'
            # ),
            Row(
                Column('about_me', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )

class AppBasicInformationForm(forms.ModelForm):
    class Meta:
        model = AppBasicInformation
        fields = ['title', 'first_name', 'middle_name', 'surname', 'date_of_birth', 'gender', 'email', 'mobile_number',
                  'native_languages', 'nationality', 'marital_status', 'currently_living_in',]
        # widgets = {
        #     'mobile': PhoneNumberPrefixWidget(attrs={'class': 'form-control textInput phone_number'}),
        # }
        labels = {
            'first_name': 'First Name(s)',
            'middle_name': 'Middle Name(s)',
            'surname': 'Surname/Last Name',
            'date_of_birth': 'Date of Birth',
            'email': 'Your Email',
            'mobile_number': 'Your Contact Number',
            'native_languages': 'Native Languages',
            'nationality': 'Your Nationality',
            'marital_status': 'Marital Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['native_languages'].help_text = 'Please select at least one. You may select ' \
                                                    'more than one language.'
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-sm-12 col-lg-3'),
                Column('first_name', css_class='form-group col-sm-12 col-lg-3'),
                Column('middle_name', css_class='form-group col-sm-12 col-lg-3'),
                Column('surname', css_class='form-group col-sm-12 col-lg-3'),
                css_class='form-row'
            ),
            Row(
                Column('date_of_birth', css_class='form-group col-sm-12 col-lg-3'),
                Column('email', css_class='form-group col-sm-12 col-lg-4'),
                # Column('mobile', css_class='form-group col-sm-12 col-lg-5'),
                Column('mobile_number', css_class='form-group col-sm-12 col-lg-5'),
                css_class='form-row'
            ),
            Row(
                Column('nationality', css_class='form-group col-sm-12 col-lg-4'),
                Column('currently_living_in', css_class='form-group col-sm-12 col-lg-4'),
                Column('gender', css_class='form-group col-sm-12 col-lg-4'),
                css_class='form-row'
            ),
            Row(
                Column('native_languages', css_class='form-group col-sm-12 col-lg-4'),
                Column('marital_status', css_class='form-group col-sm-12 col-lg-4'),
                css_class='form-row'
            ),
        )

class AppBasicEducationForm(forms.ModelForm):
    LAST_QUALIFICATION = (
        ('', 'Select'),
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
        model = AppBasicInformation
        fields = ['currently_studying', 'last_qualification', 'current_or_last_school_name', 'what_are_you_studying']
        labels = {
            'currently_studying': 'Are you currently studying?',
            'current_or_last_school_name': 'Last school name',
            'what_are_you_studying': 'At what level are you currently studying?*',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('currently_studying', css_class='form-group col-sm-12 col-lg-4'),
                Column('what_are_you_studying', css_class='form-group col-sm-12 col-lg-4 div_what_are_you_studying'),
                Column('last_qualification', css_class='form-group col-sm-12 col-lg-4 div_last_qualification'),
                Column('current_or_last_school_name', css_class='form-group col-sm-12 col-lg-4'),
                css_class='form-row'
            ),
        )



class NextOfKinInformationForm(forms.ModelForm):
    class Meta:
        model = AppBasicInformation
        fields = ['next_of_kin_name', 'relationship_to_student', 'next_of_kin_email', 'next_of_kin_phone']
        widgets = {
            'next_of_kin_phone': PhoneNumberPrefixWidget(
                attrs={'class': 'form-control textInput phone_number'}),

        }
        labels = {
            'next_of_kin_name': 'Name of your Next of Kin',
            'relationship_to_student': 'Relationship to Student',
            'next_of_kin_email': 'Next of Kin Email',
            'next_of_kin_phone': 'Next of Kin Phone',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('next_of_kin_name', css_class='form-group col-sm-12 col-lg-6'),
                Column('relationship_to_student', css_class='form-group col-sm-12 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('next_of_kin_email', css_class='form-group col-sm-12 col-lg-6'),
                Column('next_of_kin_phone', css_class='form-group col-sm-12 col-lg-6'),
                css_class='form-row'
            ),

        )

class AppAddressForm(forms.ModelForm):
    class Meta:
        model = AppAddress
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'postcode', 'country']
        labels = {
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2',
            'postcode': 'Pincode/Zipcode/Postal Code',
            'country': 'Country (Applicant is currently living in)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('address_line_1', css_class='form-group col-sm-12 col-lg-12 address'),
                css_class='form-row'
            ),
            Row(
                Column('address_line_2', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('city', css_class='form-group col-sm-6 col-lg-6'),
                Column('state', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('postcode', css_class='form-group col-sm-6 col-lg-6'),
                Column('country', css_class='form-group col-sm-6 col-lg-6 language'),
                css_class='form-row'
            ),

        )


class AppPassportInformationForm(forms.ModelForm):
    class Meta:
        model = AppPassportInformation

        fields = ['passport_number', 'issue_date', 'expiry_date', 'place_of_birth', 'issuing_authority', 'passport']

        labels = {
            'passport_number': 'Applicant Passport Number',
            'issue_date': 'Issue Date',
            'expiry_date': 'Expiry Date',
            'place_of_birth': 'Place of Birth',
            'issuing_authority': 'Issuing Authority',
            'passport': 'Upload a photocopy/scanned copy of applicant\'s  passport',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('passport_number', css_class='form-group col-sm-6 col-lg-6 address'),
                Column('passport', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('issue_date', css_class='form-group col-sm-6 col-lg-6'),
                Column('expiry_date', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('place_of_birth', css_class='form-group col-sm-6 col-lg-6'),
                Column('issuing_authority', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
        )


class AppEducationForm(forms.ModelForm):
    specify_qualification_name = forms.CharField(required=True, label='Qualification Achieved', widget=forms.Select())

    class Meta:
        model = AcademicQualification
        fields = ['institute_name', 'specify_qualification_name', 'is_currently_studying', 'qualification_achieved',
                  'grades_achieved', 'course_duration_from_year',
                  'course_duration_from_month', 'course_duration_to_month', 'course_duration_to_year',
                  'institute_email', 'institute_website', 'institute_address', 'country', 'certificate_doc_url',
                  'transcripts_doc_url']
        widgets = {
            'course_duration_from': DateInput(),
            'course_duration_to': DateInput(),
        }
        labels = {
            'institute_name': 'Institute Name',
            'is_currently_studying': 'Are you currently studying this subject?',
            'qualification_achieved': 'Type Qualification here',
            'grades_achieved': 'Grades/Score Achieved or Predicted',
            'course_duration_from_month': 'Course Duration <span class="font-weight-bold">From</span> (select month)',
            'course_duration_to_month': 'Course Duration <span class="font-weight-bold">To</span> (select month)',
            'course_duration_from_year': 'Course Duration <span class="font-weight-bold">From</span> (select year)',
            'course_duration_to_year': 'Course Duration <span class="font-weight-bold">To</span> (select year)',
            'institute_email': 'Institute Email (if known)',
            'institute_website': 'Institute Website (if known)',
            'institute_address': 'Institute Address (optional)',
            'certificate_doc_url': 'Certificate',
            'transcripts_doc_url': 'Transcripts',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('country', css_class='form-group col-sm-12 col-md-6 col-lg-6'),
                Column('is_currently_studying', css_class='form-group col-sm-12 col-md-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column(Field('specify_qualification_name', css_class='specify_qualification_name'),
                       css_class='form-group col-sm-6 col-lg-6 '),
                Column(Field('qualification_achieved', css_class='qualification_achieved'),
                       css_class='form-group col-sm-6 col-lg-6 qualification_div'),
                Column('grades_achieved', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('course_duration_from_month', css_class='form-group col-sm-6 col-lg-3'),
                Column('course_duration_from_year', css_class='form-group col-sm-6 col-lg-3'),
                Column('course_duration_to_month', css_class='form-group col-sm-6 col-lg-3'),
                Column('course_duration_to_year', css_class='form-group col-sm-6 col-lg-3'),
                css_class='form-row'
            ),
            Row(
                Column('institute_name', css_class='form-group col-sm-12 col-md-6 col-lg-6'),
                Column('institute_email', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('institute_website', css_class='form-group col-sm-6 col-lg-6'),
                Column('institute_address', css_class='form-group col-sm-12 col-md-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('certificate_doc_url', css_class='form-group col-sm-12 col-md-12 col-lg-6'),
                Column('transcripts_doc_url', css_class='form-group col-sm-12 col-md-12 col-lg-6'),
                css_class='form-row'
            ),
            'id',
        )


class DirectApplicationsForm(forms.ModelForm):
    institute = forms.ModelChoiceField(empty_label="Select Institute",
                                       queryset=Institute.objects.all(), required=False)

    class Meta:
        model = ConsideredApplication
        fields = ['institute', 'course_name']
        labels = {
            'course_name': 'Enter the course name or course code (if known)',
            'institute': 'Institute Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('institute', css_class='form-group col-sm-12 col-md-6 col-lg-6 institute-select'),
                Column('course_name', css_class='form-group col-sm-12 col-md-6 col-lg-6'),
                css_class='form-row'
            ),
            'id',

        )


class AppTrainingCertificatesForm(forms.ModelForm):
    class Meta:
        model = ProfessionalTrainingCertificate
        exclude = ['app']

        labels = {
            'certificate_name': 'Certificate Name',
            'certificate_url': 'Upload Certificate',
            'certificate_date': 'Certificate Date',
            'company_institute': 'Company/Institute Name'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('certificate_name', css_class='form-group col-sm-6 col-md-12 col-lg-6'),
                Column('company_institute', css_class='form-group col-sm-6 col-md-12 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('certificate_date', css_class='form-group col-sm-6 col-lg-6'),
                Column('certificate_url', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            'id',
        )


class AppWorkExperienceForm(forms.ModelForm):
    brief_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False,
                                        label='Job Description in Brief')

    class Meta:
        model = ProfessionalExperience
        fields = ['company_employer_name', 'position', 'duration_from_month', 'duration_from_year', 'duration_to_month',
                  'duration_to_year', 'company_email', 'company_phone', 'company_website', 'brief_description']
        widgets = {
            'duration_from': DateInput(),
            'duration_to': DateInput(),
            'company_phone': PhoneNumberPrefixWidget(
                attrs={'class': 'form-control textinput textInput form-control phone_number'}),
        }
        labels = {
            'company_employer_name': 'Company/Employer\'s Name',
            'duration_from_month': 'Duration From (month)',
            'duration_from_year': 'Duration From (year)',
            'duration_to_month': 'Duration To (month)',
            'duration_to_year': 'Duration To (year)',
            'company_email': 'Company Email',
            'company_phone': 'Company Phone',
            'company_website': 'Company Website',
            'brief_description': 'Job Description in Brief',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('company_employer_name', css_class='form-group col-sm-12 col-md-6 col-lg-6'),
                Column('position', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('duration_from_month', css_class='form-group col-sm-6 col-lg-2'),
                Column('duration_from_year', css_class='form-group col-sm-6 col-lg-4'),
                Column('duration_to_month', css_class='form-group col-sm-6 col-lg-2'),
                Column('duration_to_year', css_class='form-group col-sm-6 col-lg-4'),
                css_class='form-row'
            ),
            Row(
                Column('company_email', css_class='form-group col-sm-2 col-lg-6'),
                Column('company_phone', css_class='form-group col-sm-4 col-lg-6 phone_field'),
                css_class='form-row'
            ),
            Row(
                Column('company_website', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('brief_description', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            'id',
        )

class WouldYouLikeGainAdditionalWorkExperience(forms.ModelForm):
    would_you_like_gain_additional_work_experience = forms.ChoiceField(choices=questions_choice,
                                                                                  widget=forms.RadioSelect(),
                                                                                  label='Would you like to to gain '\
                                                                                        'additional '\
                                                                                        'work-experience/Internship to'\
                                                                                        ' enhance your career options?',
                                                                                  required=True)

    class Meta:
        model = Application
        fields = ['would_you_like_gain_additional_work_experience']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('would_you_like_gain_additional_work_experience', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )


class WouldYouBeInterestedInSharingYourDetailsWithInstitute(forms.ModelForm):
    would_you_be_interested_in_sharing_your_details_with_institute = forms.ChoiceField(choices=questions_choice,
                                                                                  widget=forms.RadioSelect(
                                                                                      attrs={'required': 'True'}),
                                                                                  label='Would you like to to gain '\
                                                                                        'additional work-experience/'\
                                                                                        'Internship to enhance your '\
                                                                                        'career options? ',
                                                                                  required=True)

    class Meta:
        model = Application
        fields = ['would_you_be_interested_in_sharing_your_details_with_institute']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('would_you_be_interested_in_sharing_your_details_with_institute',
                       css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )

class app_references_form(forms.ModelForm):
    class Meta:
        model = Reference
        exclude = ['app', 'capacity_knew_under']
        widgets = {
            'duration_from': DateInput(),
            'duration_to': DateInput(),
            'phone': PhoneNumberPrefixWidget(attrs={'class': 'form-control textInput phone_number'}),
        }
        labels = {
            'referee_name': 'Referee Name',
            'email': 'Referee\'s Email',
            'company_or_school': 'Company/School Name',
            'phone': 'Referee\'s Phone (if known)',
            'website': 'Referee\'s Website (if known)',
            'position': 'Referee\'s Position (Eg. capacity do you know this Referee)',
            'duration_from_month': 'Duration From (month)',
            'duration_from_year': 'Duration From (year)',
            'duration_to_month': 'Duration To (month)',
            'duration_to_year': 'Duration To (year)',
            'reference_upload': 'Upload a photocopy/scanned copy of this reference (if available)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['website'].help_text = "ie. the website of the institution/company where this Referee is from."
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('referee_name', css_class='form-group col-sm-12 col-md-6 col-lg-6'),
                Column('company_or_school', css_class='form-group col-sm-12 col-md-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('position', css_class='form-group col-sm-12 col-lg-6'),
                Column('email', css_class='form-group col-sm-12 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('phone', css_class='form-group col-sm-12 col-lg-4 phone_field'),
                Column('website', css_class='form-group col-sm-12 col-lg-4'),
                Column('country', css_class='form-group col-sm-12 col-lg-4'),
                css_class='form-row'
            ),
            Row(
                Column('duration_from_month', css_class='form-group col-sm-12 col-lg-2'),
                Column('duration_from_year', css_class='form-group col-sm-12 col-lg-4'),
                Column('duration_to_month', css_class='form-group col-sm-12 col-lg-2'),
                Column('duration_to_year', css_class='form-group col-sm-12 col-lg-4'),
                css_class='form-row'
            ),
            Row(
                Column('reference_upload', css_class='form-group col-sm-12 col-lg-12'),
                css_class='form-row'
            ),
            'id',
        )


class AppEnglishLanguageForm(forms.ModelForm):
    have_valid_certificate = forms.ChoiceField(choices=questions_choice,
                                               widget=forms.RadioSelect(attrs={'required': 'required', }),
                                               label='Do you have a valid English language test certificate in place?',
                                               required=True, )
    have_test_booking_date = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                               label='Do you have a test booking date in the future?*',
                                               required=False)

    class Meta:
        model = EnglishLanguage
        fields = ['have_valid_certificate', 'have_test_booking_date', 'certificate_name', 'certificate_date',
                  'listening', 'reading', 'writing', 'speaking', 'overall',
                  'certificate']

        labels = {
            'have_valid_certificate': 'Do you have a valid English language test certificate in place?',
            'have_test_booking_date': 'Do you have a test booking date in the future?*',
            'certificate_name': 'Certificate Name*',
            'certificate_date': 'Certificate Date*',
            'listening': 'Listening Score/Band*',
            'reading': 'Reading Score/Band*',
            'writing': 'Writing Score/Band*',
            'speaking': 'Speaking Score/Band*',
            'overall': 'Overall Score/Band*',
            'certificate': 'Upload a photocopy/scanned copy of this certificate (if available)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        request = get_current_request()
        if request.user.user_type == 5:
            self.fields[
                'have_valid_certificate'].label = "Do the Applicant have a valid English language test certificate in " \
                                                  "place? "
            self.fields['have_test_booking_date'].label = "Does the Applicant have a test booking date in the future?"
        self.helper.layout = Layout(
            Row(
                Column('have_valid_certificate', css_class='form-group col-md-6 col-lg-6'),
                Column('have_test_booking_date', css_class='form-group col-md-6 col-lg-6 have_test_booking_date'),
                css_class='form-row'
            ),
            Row(
                Column('certificate_name', css_class='form-group col-md-6 col-lg-6 test-name'),
                Column('certificate_date', css_class='form-group col-md-6 col-lg-6 test-date'),
                css_class='form-row'
            ),
            HTML('<div class=english_test_form>'),
            Row(
                Column('listening', css_class='form-group col-sm-3 col-lg-3'),
                Column('reading', css_class='form-group col-sm-3 col-lg-3'),
                Column('writing', css_class='form-group col-sm-3 col-lg-3'),
                Column('speaking', css_class='form-group col-sm-3 col-lg-3'),
                css_class='form-row'
            ),
            Row(
                Column('overall', css_class='form-group col-md-6 col-lg-6'),
                Column('certificate', css_class='form-group col-md-6 col-lg-6'),
                css_class='form-row'
            ),
            HTML('</div>'),
        )

class WouldYouLikeOurAlumniToAssistYouInEnglishSkillsForm(forms.ModelForm):
    would_you_like_our_alumni_to_assist_you_in_english_skills = forms.ChoiceField(choices=questions_choice,
                                                                                  widget=forms.RadioSelect(),
                                                                                  label='Would you like our Alumni to'\
                                                                                        ' assist you to improve your'\
                                                                                        ' English Language skills?',
                                                                                  required=True)

    class Meta:
        model = Application
        fields = ['would_you_like_our_alumni_to_assist_you_in_english_skills']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('would_you_like_our_alumni_to_assist_you_in_english_skills', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )


class AppPersonalStatementForm(forms.ModelForm):
    class Meta:
        model = PersonalStatement
        fields = ['question_1', 'question_2', 'question_3', 'other_information']
        labels = {
            'question_1': 'This personal statement will be viewed by universities so they can discover more about you.'
                          ' Please be advised not to include any personal contact details or names of any specific universities',
            'question_2': 'Why have you interested in this particular course or subject?',
            'question_3': 'Tell us more about your interests, hobbies, and other experiences and activities you’ve '
                          'participated in, which you think will help you to succeed in your studies with us.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        request = get_current_request()
        if request.user.user_type == 5:
            self.fields[
                'question_1'].label = "This personal statement will be viewed by universities so they can discover more about the Applicant. " \
                                      "Please be advised not to include any personal contact details or names of any specific universities"
            self.fields[
                'question_3'].label = "Tell us more about the Applicant's interests, hobbies, and other experiences " \
                                      "and activities he/she has participated in, which you think will help his/her " \
                                      "to succeed in their studies with us. "
        self.fields['question_1'].widget.attrs[
            'placeholder'] = 'If you have any other information that you would like to add to your application, ' \
                             'please enter it here. '
        self.fields['question_2'].widget.attrs[
            'placeholder'] = 'If you have any other information that you would like to add to your application, ' \
                             'please enter it here. '
        self.fields['question_3'].widget.attrs[
            'placeholder'] = 'If you have any other information that you would like to add to your application, ' \
                             'please enter it here. '
        self.fields['other_information'].widget.attrs[
            'placeholder'] = 'If you have any other information that you would like to add to your application, ' \
                             'please enter it here. '
        self.helper.layout = Layout(
            Row(
                Column('question_1', css_class='form-group col-sm-12 col-md-12 col-lg-12'),
                Column('question_2', css_class='form-group col-sm-12 col-md-12 col-lg-12'),
                Column('question_3', css_class='form-group col-sm-12 col-md-12 col-lg-12'),
                Column('other_information', css_class='form-group col-sm-12 col-md-12 col-lg-12'),
                css_class='form-row'
            ),
            'id',
        )


class AppVisaHistoryForm(forms.ModelForm):
    have_you_studied_in_the_uk_before = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect())

    class Meta:
        model = VisaHistory
        exclude = ['app', 'study_destination_country']
        widgets = {
            'visa_duration_from': DateInput(),
            'visa_duration_to': DateInput(),
            'reason': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'have_you_studied_in_the_uk_before': 'Have you studied in the United Kingdom before?',
            'visa_duration_from_year': 'Visa Duration From (select year)*',
            'visa_duration_from_month': 'Visa Duration From (select month)*',
            'visa_duration_to_year': 'Visa Duration To (select year)*',
            'visa_duration_to_month': 'Visa Duration To (select month)*',
            'have_you_ever_been_refuse_entry_in_to_the_uk': 'Have you ever been refused entry into any country before?',
            'have_you_ever_been_deported_from_the_uk': 'Have you ever been deported from any country?',
            'reason': 'Please provide reason',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        request = get_current_request()
        study_destination_country = self.instance.study_destination_country
        temp = 'Have you' if request.user.user_type == 3 else 'Has the Applicant'
        self.fields['have_you_studied_in_the_uk_before'].label = temp + ' studied in ' + getifneedtheartical(
            study_destination_country.code) + study_destination_country.name + ' before?'
        self.fields[
            'have_you_ever_been_refuse_entry_in_to_the_uk'].label = temp + ' ever been refused entry into ' + getifneedtheartical(
            study_destination_country.code) + study_destination_country.name + ' before?'
        self.fields[
            'have_you_ever_been_deported_from_the_uk'].label = temp + ' ever been deported from ' + getifneedtheartical(
            study_destination_country.code) + study_destination_country.name + '?'
        self.helper.layout = Layout(
            Row(
                Column('have_you_studied_in_the_uk_before', css_class='form-group col-sm-12 col-md-12 col-lg-12'),
                css_class='form-row'
            ),
            Row(
                Column('visa_duration_from_month', css_class='form-group col-sm-3 col-lg-3'),
                Column('visa_duration_from_year', css_class='form-group col-sm-3 col-lg-3'),
                Column('visa_duration_to_month', css_class='form-group col-sm-3 col-lg-3'),
                Column('visa_duration_to_year', css_class='form-group col-sm-3 col-lg-3'),
                css_class='form-row duration'
            ),
            Row(
                Column('have_you_ever_been_refuse_entry_in_to_the_uk', css_class='form-group col-sm-6 col-lg-6'),
                Column('have_you_ever_been_deported_from_the_uk', css_class='form-group col-sm-6 col-lg-6'),
                css_class='form-row'
            ),
            Row(
                Column('reason', css_class='form-group reason col-sm-12 col-md-12 col-lg-12'),
                css_class='form-row'
            ),
            'id',
        )


class AppAdditionalInformationForm(forms.ModelForm):
    learning_disabilities_or_difficulties = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                                              label='Does the Applicant have any learning '
                                                                    'disabilities or difficulties?')
    health_conditions = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                          label='Does the Applicant have any health conditions?')
    criminal_records = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(),
                                         label='Does the Applicant have any criminal records?')

    class Meta:
        model = Application
        fields = ['learning_disabilities_or_difficulties', 'disabilities_text', 'health_conditions',
                  'health_conditions_text', 'criminal_records', 'records', 'others', 'ethnic_origin',
                  'religion_or_belief', 'sexual_orientation'
                  ]
        labels = {
            'health_conditions_text': 'Please provide details here',
            'disabilities_text': 'Please provide details here',
            'research_portfolio': 'Phd Proposal',
            'records': 'Please share this records here',
            'others': 'Additional notes to support this application (if any)',
            'ethnic_origin': 'What is your ethnic origin?',
            'religion_or_belief': 'What is your religion or belief?',
            'sexual_orientation': 'What is your sexual orientation?',
        }
        widgets = {
            'records': forms.Textarea(attrs={'rows': 2}),
            'health_conditions_text': forms.Textarea(attrs={'rows': 2}),
            'disabilities_text': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('learning_disabilities_or_difficulties', css_class='form-group col-sm-12 col-md-5 col-lg-5'),
                Column('disabilities_text', css_class='form-group col-sm-12 col-md-7 col-lg-7'),
                css_class='form-row'
            ),
            Row(
                Column('health_conditions', css_class='form-group col-sm-12 col-md-5 col-lg-5'),
                Column('health_conditions_text', css_class='form-group col-sm-12 col-md-7 col-lg-7'),
                css_class='form-row'
            ),
            Row(
                Column('criminal_records', css_class='form-group col-sm-12 col-md-5 col-lg-5'),
                Column('records', css_class='form-group col-sm-12 col-md-7 col-lg-7'),
                css_class='form-row'
            ),

            Row(
                Column('others', css_class='form-group col-sm-12 col-md-12 col-lg-12'),
                css_class='form-row'
            ),
            HTML(
                '<h5>Universities have equal opportunity & diversity policies in place and may require the following '
                'information:</h5>'),
            HTML('<div class="line-2"></div>'),
            Row(
                Column('ethnic_origin', css_class='form-group col-sm-12 col-md-4 col-lg-4'),
                Column('religion_or_belief', css_class='form-group col-sm-12 col-md-4 col-lg-4'),
                Column('sexual_orientation', css_class='form-group col-sm-12 col-md-4 col-lg-4'),
                css_class='form-row'
            ),
        )


class AppInstituteFeedbackForm(forms.ModelForm):
    class Meta:
        model = ConsideredApplication
        fields = ['app_status_by_institute', 'feedback_comment']


class AppInstituteRejectForm(forms.ModelForm):
    specify_offer_reject_reason = forms.CharField(required=False, label='Specify offer reject reason*')

    class Meta:
        model = ConsideredApplication
        fields = ['offer_reject_reason', 'specify_offer_reject_reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Column(Field('offer_reject_reason', css_class='offer_reject_reason'),
                   css_class='form-group col-md-12 mb-0'),
            Column(Field('specify_offer_reject_reason', css_class='specify_offer_reject_reason'),
                   css_class='form-group col-md-12 mb-0 specify_offer_reject_reason_div'),
        )

    def clean(self):
        if self.cleaned_data['offer_reject_reason'] == 'Other' and not self.cleaned_data['specify_offer_reject_reason']:
            msg = "Please specify the specify offer reject reason."
            self.add_error('specify_offer_reject_reason', msg)


class AppCommentForm(forms.ModelForm):
    class Meta:
        model = ApplicationComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 5}),
        }


class OfferFinalSelection(forms.ModelForm):
    class Meta:
        model = FinalSelected
        fields = ['payment_date', 'amount_paid', 'payment_reference', 'proof_of_payment']
        widgets = {
            'payment_date': DateInput(),
        }
        labels = {
            'amount_paid': 'Amount Paid (In GBP)',
        }


class AppAdditionalDocumentsForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ['type', 'doc_type', 'name', 'upload']
        labels = {
            'type': 'Document Type*',
            'doc_type': 'Write Document Type Here*',
            'name': 'Document Name',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['upload'].help_text = "Keep the filesize under 5 MB."
        self.helper.form_tag = False
        self.helper.layout = Layout(

            Row(
                Column('type', css_class='form-group col-sm-12 col-md-4 col-lg-4'),
                Column('doc_type', css_class='form-group col-sm-12 col-md-4 col-lg-4 doc_type'),
                Column('name', css_class='form-group col-sm-12 col-md-4 col-lg-4'),
                Column('upload', css_class='form-group col-sm-12 col-md-4 col-lg-4'),
                css_class='form-row'
            ),
        )


class ApplicationFeedbackForm(forms.ModelForm):
    FEEDBACK_CHOICES = (
        (0, 'Poor'),
        (1, 'Satisfactory'),
        (2, 'Good'),
        (3, 'Very Good'),
        (4, 'Excellent'),
    )
    q1 = forms.ChoiceField(choices=FEEDBACK_CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-inline'}), label="1. How was your communication with your mentor?", required=False)
    q2 = forms.ChoiceField(choices=FEEDBACK_CHOICES, widget=forms.RadioSelect(
        attrs={'class': 'form-check-inline'}), label='2. How was your overall experience with our platform?',
                           required=False)
    q3 = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(
        attrs={'class': 'form-check-inline'}), label='3. Will you recommend this mentor to others? ', required=False)
    q4 = forms.ChoiceField(choices=questions_choice, widget=forms.RadioSelect(
        attrs={'class': 'form-check-inline'}), label='4. Will you recommend this platform to others?', required=False)

    class Meta:
        model = ApplicationFeedback
        fields = ['q1', 'q2', 'q3', 'q4']
