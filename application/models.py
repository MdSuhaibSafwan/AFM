import datetime
from django.contrib.auth import user_logged_out, user_logged_in
from django.db import models
# Create your models here.
from administration.models import *
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from django_countries import Countries
from AFM.validators import validate_file_size

area_of_study_choice = (
    (6, 'Medicine'),
)

level_of_english_choices = (
    ('', 'Select'),
    (0, 'Beginners'),
    (1, 'Elementary'),
    (2, 'Intermediate'),
    (3, 'Advanced'),
    (4, 'Native Speaker'),
)

intake_month_choices = (
    ('', 'Select'),
    (0, 'January'),
    (1, 'February'),
    (2, 'March'),
    (3, 'April'),
    (4, 'May'),
    (5, 'June'),
    (6, 'July'),
    (7, 'August'),
    (8, 'September'),
    (9, 'October'),
    (10, 'November'),
    (11, 'December'),
)

profile_status_choices = (
    (0, 'Approved'),
    (1, 'Rejected'),
    (2, 'Completed'),
    (3, 'Incomplete'),
)

questions_choice = (
    (0, 'NO'),
    (1, 'YES'),
)

programme_level_choices_student = (
    ('', 'Select'),
    (0, 'Foundation'),
    (1, 'Undergraduate'),
    (2, 'Postgraduate'),
    (3, 'Research'),
)
programme_level_choices_mentor = (
    ('', 'Select'),
    (0, 'SSC'),
    (1, 'HSC'),
    (2, 'A Level'),
    (3, 'GCSE'),
    (4, 'Bachelors'),
    (5, 'Masters'),
    (6, 'PhD'),
    (7, 'Diploma'),
    (8, 'International Year'),
    (9, 'Associate Degree'),
    (10, 'Professional Certificate'),
)
FEES_CHOICE = (
    ('', 'Select'),
    ('0 - £5,000', '0 - £5,000'),
    ('£5,000 - £10,000', '£5,000 - £10,000'),
    ('£10,000 - £20,000', '£10,000 - £20,000'),
    ('£20,000 - £30,000', '£20,000 - £30,000'),
    ('£30,000 - £50,000', '£30,000 - £50,000'),
)
ETHNIC_ORIGIN_CHOICES = (
    ('', 'Select'),
    ('Arab', 'Arab'),
    ('Asian - Indian', 'Asian - Indian'),
    ('Asian - Pakistani', 'Asian - Pakistani'),
    ('Asian - Bangladeshi', 'Asian - Bangladeshi'),
    ('Asian - Chinese', 'Asian - Chinese'),
    ('Asian - Other', 'Asian - Other'),
    ('Black - Caribbean', 'Black - Caribbean'),
    ('Black - African', 'Black - African'),
    ('Black - Other', 'Black - Other'),
    ('Gypsy, Traveller or', 'Gypsy, Traveller or'),
    ('White', 'White'),
    ('White/Black Caribbn', 'White/Black Caribbn'),
    ('White/Black African', 'White/Black African'),
    ('White and Asian', 'White and Asian'),
    ('Other Mixed', 'Other Mixed'),
    ('Other', 'Other'),
    ('Prefer not to say', 'Prefer not to say'),
)
RELIGION_OR_BELIEF_CHOICES = (
    ('', 'Select'),
    ('Any other religion or belief', 'Any other religion or belief'),
    ('Buddhist', 'Buddhist'),
    ('Christian', 'Christian'),
    ('Christian - Church of Ireland', 'Christian - Church of Ireland'),
    ('Christian - Church of Scotland', 'Christian - Church of Scotland'),
    ('Christian - Methodist Church in Ireland', 'Christian - Methodist Church in Ireland'),
    ('Christian - Other denomination', 'Christian - Other denomination'),
    ('Christian - Presbyterian Church in Ireland', 'Christian - Presbyterian Church in Ireland'),
    ('Christian - Roman Catholic', 'Christian - Roman Catholic'),
    ('Hindu', 'Hindu'),
    ('Jewish', 'Jewish'),
    ('Muslim', 'Muslim'),
    ('No religion', 'No religion'),
    ('Sikh', 'Sikh'),
    ('Spiritual', 'Spiritual'),
    ('Prefer not to say', 'Prefer not to say'),
)
SEXUAL_ORIENTATION_CHOICES = (
    ('', 'Select'),
    ('Bisexual', 'Bisexual'),
    ('Gay Man', 'Gay Man'),
    ('Gay Woman', 'Gay Woman'),
    ('Heterosexual', 'Heterosexual'),
    ('Other', 'Other'),
    ('Prefer not to say', 'Prefer not to say'),
)


class DestinationCountries(Countries):
    only = [
        'GB', 'US', 'AU', 'CA', 'HR', 'CZ', 'HU', 'IT', 'LV', 'PL', 'SK', 'ES',
    ]


class Application(models.Model):
    slug = models.CharField(null=True, unique=True, max_length=50, )
    admin = models.ForeignKey('administration.CustomUser', primary_key=False, on_delete=models.CASCADE, null=True,
                              related_name="application")
    mentor = models.ForeignKey('administration.Mentor', on_delete=models.SET_NULL, null=True,
                               related_name="application_mentor")
    consent_as_parent = models.BooleanField(null=True)
    consent_terms_condition = models.BooleanField(null=True)

    # Multi select
    program_level = models.PositiveIntegerField(choices=programme_level_choices_student, null=True)
    selected_institutes = models.ManyToManyField('administration.Institute', related_name='selected_institutes')
    exclude_institutes = models.ManyToManyField('administration.Institute', related_name='exclude_institutes',
                                                blank=True)
    exclude_institutes_other = models.CharField(null=True, blank=True, max_length=500)

    allow_other_institutes = models.IntegerField(null=True, choices=questions_choice, default=1)
    subject = models.IntegerField(null=True, choices=area_of_study_choice, default=6, blank=True)
    desire_course = models.CharField(max_length=200, blank=True, null=True)
    YEAR_CHOICES = [('', 'Select')]
    for r in range(datetime.datetime.now().year + 1, (datetime.datetime.now().year + 10)):
        YEAR_CHOICES.append((r, r))

    intake_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year + 1, null=True)
    DESIRED_MONTH_CHOICES = (
        ('', 'Select'),
        (0, 'January'),
        (8, 'September'),
    )
    intake_month = models.PositiveIntegerField(null=True, choices=DESIRED_MONTH_CHOICES)
    study_destination_country = CountryField(blank_label='Select country', multiple=True, default='GB',
                                             countries=DestinationCountries)
    fees_affordability = models.CharField(null=True, max_length=30, choices=FEES_CHOICE, default='£10,000 - £20,000')
    scholarship_option = models.IntegerField(null=True, choices=questions_choice, default=1)
    about_me = models.TextField(null=True, blank=True)
    level_of_english = models.IntegerField(null=True, choices=level_of_english_choices)
    # Additional Information / Requirements
    learning_disabilities_or_difficulties = models.IntegerField(null=True, choices=questions_choice)
    disabilities_text = models.TextField(null=True, blank=True)
    health_conditions = models.CharField(max_length=30, null=True)
    health_conditions_text = models.TextField(null=True, blank=True)
    criminal_records = models.IntegerField(null=True, choices=questions_choice)
    records = models.CharField(max_length=100, null=True, blank=True)
    others = models.TextField(null=True, blank=True)
    ethnic_origin = models.CharField(max_length=100, null=True, blank=True, choices=ETHNIC_ORIGIN_CHOICES)
    religion_or_belief = models.CharField(max_length=100, null=True, blank=True, choices=RELIGION_OR_BELIEF_CHOICES)
    sexual_orientation = models.CharField(max_length=100, null=True, blank=True, choices=SEXUAL_ORIENTATION_CHOICES)
    # Additional Documents
    research_portfolio = models.FileField(null=True, upload_to='research-portfolios/', validators=[validate_file_size])
    portfolio = models.FileField(null=True, upload_to='portfolios/', blank=True, validators=[validate_file_size])

    status = models.IntegerField(choices=profile_status_choices, null=True)
    approved_by = models.ForeignKey('administration.AppAdmin', on_delete=models.SET_NULL, null=True, )
    is_lead = models.ForeignKey('administration.Lead', on_delete=models.SET_NULL, null=True, blank=True)
    institute = models.ManyToManyField('administration.Institute', related_name='institute')
    fill_form_permission = models.BooleanField(default=False, null=True)

    applypool_status = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    submitted_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "application"


class DirectApplication(models.Model):
    app = models.ForeignKey(Application, primary_key=False, on_delete=models.CASCADE, null=True,
                            related_name='direct_application')
    institute = models.ForeignKey('administration.Institute', on_delete=models.CASCADE, null=True,
                                  related_name='direct_app_institute')
    course_name = models.CharField(max_length=50, null=True, blank=True)


class EnglishLanguage(models.Model):
    app = models.OneToOneField(Application, on_delete=models.CASCADE, null=True, related_name='english_language')
    have_valid_certificate = models.IntegerField(null=True, choices=questions_choice)
    have_test_booking_date = models.IntegerField(null=True, choices=questions_choice, blank=True, default=0)
    certificate_name = models.CharField(max_length=50, null=True, blank=True)
    certificate_date = models.DateField(null=True, blank=True)
    listening = models.CharField(max_length=3, null=True, blank=True)
    reading = models.CharField(max_length=3, null=True, blank=True)
    writing = models.CharField(max_length=3, null=True, blank=True)
    speaking = models.CharField(max_length=3, null=True, blank=True)
    overall = models.CharField(max_length=3, null=True, blank=True)
    score = models.CharField(max_length=3, null=True, blank=True)
    certificate = models.FileField(upload_to='english-language-certificates/', null=True, blank=True, validators=[validate_file_size])

    def __str__(self):
        return str(self.id)


class VisaHistory(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, related_name='visa_history_app')
    study_destination_country = CountryField(blank_label='Select country', default='GB')
    have_you_studied_in_the_uk_before = models.IntegerField(null=True, choices=questions_choice)
    VISA_TYPE = (
        ('', 'Select'),
        ('Student Visa', 'Student Visa'),
        ('Visit Visa', 'Visit Visa'),
    )
    visa_type = models.CharField(max_length=50, choices=VISA_TYPE, null=True, blank=True)
    reason = models.CharField(max_length=100, null=True, blank=True)
    # visa_duration_from = models.DateField(null=True)
    # visa_duration_to = models.DateField(null=True)

    YEAR_CHOICES = [('', 'Select')]
    for r in range((datetime.datetime.now().year - 20), (datetime.datetime.now().year + 3)):
        YEAR_CHOICES.append((r, r))
    visa_duration_from_year = models.IntegerField(choices=YEAR_CHOICES, null=True,
                                                  blank=True)
    visa_duration_from_month = models.PositiveIntegerField(null=True, choices=intake_month_choices, blank=True)
    visa_duration_to_year = models.IntegerField(choices=YEAR_CHOICES, null=True,
                                                blank=True)
    visa_duration_to_month = models.PositiveIntegerField(null=True, choices=intake_month_choices, blank=True)

    # course_duration_from_month = models.PositiveIntegerField(null=True, choices=intake_month_choices)
    have_you_ever_been_refuse_entry_in_to_the_uk = models.IntegerField(null=True, choices=questions_choice)

    have_you_ever_been_deported_from_the_uk = models.IntegerField(null=True, choices=questions_choice)

    def __str__(self):
        return str(self.id)


class Reference(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, related_name='references_app')
    referee_name = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=50, null=True)
    company_or_school = models.CharField(max_length=50, null=True)
    country = CountryField(blank_label='Select country', null=True)
    email = models.EmailField(max_length=50, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)
    capacity_knew_under = models.CharField(max_length=50, null=True, blank=True)
    # duration_from = models.DateField(null=True)
    YEAR_CHOICES = [('', 'Select')]
    for r in range((datetime.datetime.now().year - 20), (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    duration_from_year = models.IntegerField(choices=YEAR_CHOICES, null=True)
    duration_from_month = models.PositiveIntegerField(null=True, choices=intake_month_choices)

    # duration_to = models.DateField(null=True)
    duration_to_year = models.IntegerField(choices=YEAR_CHOICES, null=True)
    duration_to_month = models.PositiveIntegerField(null=True, choices=intake_month_choices)
    reference_upload = models.FileField(upload_to='references/', null=True, blank=True, validators=[validate_file_size])

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "references_app"


class ProfessionalExperience(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True,
                            related_name='professional_experience_app')
    company_employer_name = models.CharField(null=True, max_length=110, blank=True)
    position = models.CharField(null=True, max_length=110, blank=True)

    # duration_from = models.DateField(null=True, )
    # duration_to = models.DateField(null=True, )

    YEAR_CHOICES = [('', 'Select')]
    for r in range((datetime.datetime.now().year - 20), (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    duration_from_year = models.IntegerField(choices=YEAR_CHOICES, null=True,
                                             blank=True)
    duration_from_month = models.PositiveIntegerField(null=True, choices=intake_month_choices, blank=True)

    duration_to_year = models.IntegerField(choices=YEAR_CHOICES, null=True,
                                           blank=True)
    duration_to_month = models.PositiveIntegerField(null=True, choices=intake_month_choices, blank=True)

    company_email = models.EmailField(null=True, max_length=50, blank=True)
    company_phone = PhoneNumberField(null=True, blank=True)
    company_address = models.CharField(null=True, max_length=110, blank=True)
    company_website = models.URLField(max_length=300, null=True, blank=True)
    brief_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "professional_experience_app"


class ProfessionalTrainingCertificate(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True,
                            related_name='professional_training_certificates_app')
    certificate_name = models.CharField(null=True, max_length=110, blank=True)
    company_institute = models.CharField(null=True, max_length=110, blank=True)
    certificate_date = models.DateField(null=True, blank=True)
    certificate_url = models.FileField(upload_to='professional-training-certificates/', null=True, blank=True, validators=[validate_file_size])

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "professional_training_certificates_app"


class AcademicQualification(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, related_name='academic_qualifications')
    institute_name = models.CharField(null=True, max_length=110, )
    is_currently_studying = models.IntegerField(null=True, choices=questions_choice, default=0)
    qualification_achieved = models.CharField(null=True, max_length=110, blank=True)
    grades_achieved = models.CharField(null=True, max_length=2, )
    # course_duration_from = models.DateField(null=True,  )
    # course_duration_to = models.DateField(null=True,  )

    YEAR_CHOICES = [('', 'Select')]
    for r in range((datetime.datetime.now().year - 10), (datetime.datetime.now().year + 1)):
        YEAR_CHOICES.append((r, r))

    course_duration_from_year = models.IntegerField(choices=YEAR_CHOICES,
                                                    null=True)
    course_duration_from_month = models.PositiveIntegerField(null=True, choices=intake_month_choices)
    COURSE_DURATION_YEAR_CHOICES = [('', 'Select')]

    for r in range((datetime.datetime.now().year - 20), (datetime.datetime.now().year + 2)):
        COURSE_DURATION_YEAR_CHOICES.append((r, r))
    course_duration_to_year = models.IntegerField(choices=COURSE_DURATION_YEAR_CHOICES, null=True)
    course_duration_to_month = models.PositiveIntegerField(null=True, choices=intake_month_choices)

    year_awarded = models.SmallIntegerField(null=True, )
    programme_level = models.IntegerField(null=True, choices=programme_level_choices_student, )
    institute_email = models.EmailField(null=True, max_length=50, blank=True)
    institute_website = models.URLField(max_length=200, null=True, blank=True)
    institute_address = models.CharField(null=True, max_length=110, blank=True)
    country = CountryField(blank_label='Select country', null=True)
    certificate_doc_url = models.FileField(upload_to='academic-qualification-certificates/', null=True, blank=True, validators=[validate_file_size])
    transcripts_doc_url = models.FileField(upload_to='transcripts/', null=True, blank=True, validators=[validate_file_size])

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "academic_qualifications"


class ApplicationFeedback(models.Model):
    app = models.OneToOneField(Application, on_delete=models.CASCADE, null=True)
    q1 = models.CharField(max_length=10, null=True)
    q2 = models.CharField(max_length=10, null=True)
    q3 = models.IntegerField(null=True, choices=questions_choice)
    q4 = models.IntegerField(null=True, choices=questions_choice)

    class Meta:
        db_table = "application_feedback"


class ApplicationOfferStatus(models.Model):
    app_status_by_institute = (
        (1, 'make a formal application'),
        (2, 'request documents'),
        (3, 'interview'),
    )
    OFFER_STATUS = (
        (0, 'In Process'),
        (1, 'Conditional'),
        (2, 'Unconditional'),
        (3, 'Unsuccessful'),
    )
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, related_name='application_offer_status')
    institute = models.ForeignKey('administration.Institute', on_delete=models.CASCADE, null=True,
                                  related_name='application_offer_status_institute')
    app_status_by_institute = models.IntegerField(null=True, choices=app_status_by_institute)
    student_response_to_application = models.CharField(null=True, max_length=110)
    feedback_comment = models.TextField(null=True)
    offer_select = models.BooleanField(default=False, null=True)
    offer_status = models.IntegerField(null=True, choices=OFFER_STATUS, default=1)
    final_selection = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "application_offer_status"


class OmittedApp(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    institute = models.ForeignKey('administration.Institute', on_delete=models.CASCADE, null=True)

    # reason_reject = models.IntegerField(null=True)

    class Meta:
        db_table = "Omitted_applications"


class ArchiveApp(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    institute = models.ForeignKey('administration.Institute', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "Archive_applications"


class ApplicationComment(models.Model):
    COMMENT_STATUS = (
        (True, 'published'),
        (False, 'draft'),
    )
    COMMENT_TYPE = ((0, 'Open'), (1, 'App Admins Only'))
    comment_type = models.IntegerField(null=True, default=0, choices=COMMENT_TYPE)
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    app_admin = models.ForeignKey('administration.CustomUser', on_delete=models.CASCADE, null=True)
    comment = models.TextField(null=True)
    comment_status = models.BooleanField(null=True, choices=COMMENT_STATUS, default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "application_comments"


class ApplicationAppliedAtUniversityLogin(models.Model):
    APPLICATION_TYPE = (
        (0, 'Online Application'),
        (1, 'Email Application'),
    )
    app_type = models.IntegerField(null=True, default=0, choices=APPLICATION_TYPE)
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True,
                            related_name='application_applied_at_university_logins')
    admin = models.ForeignKey('administration.CustomUser', on_delete=models.CASCADE, null=True)
    institute = models.ForeignKey('administration.Institute', on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=50, null=True, blank=True)
    institute_url = models.URLField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    reference_id = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    application_doc = models.FileField(upload_to='email-applications/', null=True, blank=True, validators=[validate_file_size])
    date = models.DateField(null=True)
    APPROVED_STATUS = (
        (0, 'In Process'),
        (1, 'Conditional'),
        (2, 'Unconditional'),
        (3, 'Unsuccessful'),
    )
    status = models.IntegerField(null=True, default=0, choices=APPROVED_STATUS)

    class Meta:
        db_table = "application applied at university logins"


class ConsideredApplication(models.Model):
    APPLICATION_TYPE = (
        (0, 'Online Application'),
        (1, 'Email Application'),
    )
    APP_RESPONSE_STATUS = (
        (1, 'make a formal application'),
        (2, 'request documents'),
        (3, 'interview'),
    )
    OFFER_STATUS = (
        (0, 'In Process'),
        (1, 'Conditional'),
        (2, 'Unconditional'),
        (3, 'Unsuccessful'),
    )
    OFFER_REJECT_REASON = (
        ('', 'Select'),
        ('Enrolled with other Institute', 'Enrolled with other Institute'),
        ('Not interested', 'Not interested'),
        ('Change of study destination country', 'Change of study destination country'),
        ('Other', 'Other'),
    )
    # Took from app_admin
    app_type = models.IntegerField(null=True, choices=APPLICATION_TYPE)
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, )
    admin = models.ForeignKey('administration.CustomUser', on_delete=models.CASCADE, null=True)
    institute = models.ForeignKey('administration.Institute', on_delete=models.CASCADE, null=True)
    course_name = models.CharField(max_length=50, null=True, blank=True)
    institute_url = models.URLField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, )
    reference_id = models.CharField(max_length=50, null=True, )
    password = models.CharField(max_length=50, null=True, blank=True)
    application_doc = models.FileField(upload_to='email-applications/', null=True, blank=True, validators=[validate_file_size])
    date = models.DateField(null=True)
    notes = models.CharField(max_length=100, null=True, blank=True)

    # Response from institute
    app_status_by_institute = models.IntegerField(null=True, choices=APP_RESPONSE_STATUS)
    feedback_comment = models.TextField(null=True)
    feedback_comment_admin = models.TextField(null=True)
    response_date = models.DateField(null=True)

    # Repsonse from student
    offer_select = models.BooleanField(default=False, null=True)
    offer_select_date = models.DateTimeField(null=True)
    offer_reject_reason = models.CharField(null=True, max_length=100, choices=OFFER_REJECT_REASON)
    offer_status = models.IntegerField(null=True, choices=OFFER_STATUS)
    final_selection = models.BooleanField(default=False, null=True)

    # Direct application or came from applypool
    is_direct_app = models.BooleanField(default=False, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.id) + ' (' + str(self.app) + ')'


class PersonalStatement(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True, related_name='personal_statement_app')
    institute = models.ForeignKey('administration.Institute', null=True, blank=True, on_delete=models.CASCADE)
    considered_application = models.ForeignKey(ConsideredApplication, null=True, blank=True, on_delete=models.CASCADE)
    question_1 = models.TextField(null=True)
    question_2 = models.TextField(null=True)
    question_3 = models.TextField(null=True)
    other_information = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


class ApplicationLog(models.Model):
    APP_STATUS = (
        (0, 'Approved'),
        (1, 'Rejected'),
        (2, 'Submitted'),
        (3, 'Incomplete'),
        (4, 'Omitted'),
        (5, 'Reconsidered'),
        (6, 'Considered By Institute'),
        (7, 'App Applied At Institute'),
        (8, 'Offer Status Change'),
        (9, 'Student Response'),
        (10, 'Final Selection'),
        (11, 'Document Upload'),
        (12, 'Document Deleted'),
    )
    app = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True)
    type = models.IntegerField(null=True, choices=APP_STATUS)
    message = models.CharField(max_length=100, null=True, blank=True)
    admin = models.ForeignKey('administration.CustomUser', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    considered_app = models.ForeignKey(ConsideredApplication, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.id)


class FinalSelected(models.Model):
    offer = models.OneToOneField(ConsideredApplication, on_delete=models.CASCADE, null=True)
    payment_date = models.DateField(null=True)
    payment_reference = models.CharField(max_length=100, null=True)
    amount_paid = models.PositiveIntegerField(null=True)
    proof_of_payment = models.FileField(upload_to='proof-of-payments/', null=True, validators=[validate_file_size])
    approve_status = models.BooleanField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)


class DocumentUpload(models.Model):
    DOCUMENT_TYPE = (
        ('', 'Select Document Type'),
        (5, 'Qualification'),
        (6, 'English Language'),
        (7, 'Training'),
        (8, 'Personal Statement'),
        (9, 'Resume/CV'),
        (10, 'Portfolio'),
        (11, 'Research Proposal'),
        (12, 'Passport/Visa Document'),
        (1, 'Conditional Offer'),
        (2, 'Unconditional Offer'),
        (4, 'Application Unsuccessful'),
        (13, 'Invoice'),
        (14, 'Proof of Payment'),
        (3, 'CAS Letter'),
        ('', 'Other'),
    )
    admin = models.ForeignKey('administration.CustomUser', on_delete=models.CASCADE, null=True)
    app = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
    type = models.IntegerField(null=True, choices=DOCUMENT_TYPE, blank=True)
    doc_type = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True)
    upload = models.FileField(null=True, upload_to='application-document-uploads/', validators=[validate_file_size])
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
