from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
import datetime
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
# from social_core.utils import slugify
from django.utils.text import slugify
from django_countries import Countries
from AFM.validators import validate_file_size


area_of_study_choice = (
    ('', 'Select'),
    (1, 'Business Studies'),
    (2, 'Social Studies'),
    (3, 'Arts & Design'),
    (4, 'Law'),
    (5, 'Biomedical Sciences'),
    (6, 'Medicine'),
    (7, 'Dentistry'),
    (8, 'Pharmacy'),
    (9, 'Computer Science'),
    (10, 'Finance'),
    (11, 'Architecture'),
    (12, 'Finance & Accounting'),
    (13, 'Nursing'),
    (14, 'Politics'),
    (15, 'Chemical Engineering'),
    (16, 'Electrical Engineering'),
    (17, 'International Relations'),
    (18, 'Mechanical Engineering'),
    (19, 'Economics'),
    (20, 'Civil Engineering'),
    (21, 'Other')
)


AP_COURSE = (
    (1, 'University Foundation Programme in Business Management'),
    (2, 'University Foundation Programme in Engineering'),
    (3, 'University Foundation Programme in Social Sciences'),
    (4, 'University Foundation Programme in Computer Science'),
    (5, 'Medical Foundation Programme')
)


def getsubject(value):
    if value == 1:
        return 'Business Studies'
    if value == 2:
        return 'Social Studies'
    if value == 3:
        return 'Arts & Design'
    if value == 4:
        return 'Law'
    if value == 5:
        return 'Biomedical Sciences'
    if value == 6:
        return 'Medicine'
    if value == 7:
        return 'August'
    if value == 8:
        return 'pharmacy'
    if value == 9:
        return 'Computer Science'
    if value == 10:
        return 'Finance'
    if value == 11:
        return 'Architecture'
    if value == 12:
        return 'Finance & Accounting'
    if value == 13:
        return 'Nursing'
    if value == 14:
        return 'Politics'
    if value == 15:
        return 'Chemical Engineering'
    if value == 16:
        return 'Electrical Engineering'
    if value == 17:
        return 'International Relations'
    if value == 18:
        return 'Mechanical Engineering'
    if value == 19:
        return 'Economics'
    if value == 20:
        return 'Civil Engineering'
    if value == 21:
        return 'Other'


level_of_english_choices = (
    ('', 'Select'),
    (0, 'Beginners'),
    (1, 'Elementary'),
    (2, 'Intermediate'),
    (3, 'Advanced'),
    (4, 'Native Speaker'),
)

gender_choices = (('', 'Select'), (0, 'Male'), (1, 'Female'), (2, 'Prefer not to say'))

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
    (0, 'approved'),
    (1, 'rejected'),
    (2, 'hold'),
)

questions_choice = (
    (0, 'NO'),
    (1, 'YES'),

)

programme_level_choices_mentor = (
    ('', 'Select'),
    (0, 'Foundation'),
    (1, 'Undergraduate'),
    (2, 'Postgraduate'),
    # (3, 'Research'),
)
programme_level_choices_student = (
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
TITLE_CHOICE = (
    ('', 'Select'),
    ('mr', 'Mr'),
    ('miss', 'Miss'),
    ('ms', 'Ms'),
    ('mrs', 'Mrs'),
    ('dr', 'Dr'),
    ('prof', 'Prof'),)

SPOKEN_LANGUAGES_CHOICES = (
    ('', 'Select'),
    ('english', 'English'),
    ('hindi', 'Hindi'),
    ('gujarati', 'Gujarati'),

)
STUDY_YEAR = (
    ('', 'Select'),
    (1, 'First Year'),
    (2, 'Second Year'),
    (3, 'Third Year'),
    (4, 'Fourth Year'),
    (5, 'Fifth Year'),
    (6, 'Sixth Year'),

)

TUTORING_SUBJECT = (
    ('', 'Select'),
    ('Maths', 'Maths'),
    ('Physics', 'Physics'),
    ('Biology', 'Biology'),
    ('Chemistry', 'Chemistry'),
    ('English', 'English'),
    ('BAMT', 'BAMT'),
    ('UCAT', 'UCAT'),
    ('GMSAT', 'GMSAT'),
    ('Economics', 'Economics'),
    ('ICT', 'ICT'),
    ('Other', 'Other')
)

YEAR_CHOICES = [('', 'Select')]
for r in range((datetime.datetime.now().year - 20), datetime.datetime.now().year):
    YEAR_CHOICES.append((r, r))


class DestinationCountries(Countries):
    only = [
        'GB', 'AE'
    ]



class SpokenLanguage(models.Model):
    language = models.CharField(unique=True, max_length=50, null=True)

    def __str__(self):
        return str(self.language)

    class Meta:
        ordering = ['language']


class Hobby(models.Model):
    hobby = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.hobby)

    class Meta:
        verbose_name_plural = "hobbies"
        ordering = ['hobby']


class FoundationProvider(models.Model):
    foundation_provider = models.CharField(unique=True, max_length=100, null=True)

    def __str__(self):
        return str(self.foundation_provider)


class SubjectFoundation(models.Model):
    subject_foundation = models.CharField(unique=True, max_length=50, null=True)

    def __str__(self):
        return str(self.subject_foundation)


class TutoringSubject(models.Model):
    tutoring_subject = models.CharField(unique=True, max_length=100, null=True)

    def __str__(self):
        return str(self.tutoring_subject)


class TutoringWith(models.Model):
    tutoring_with = models.CharField(unique=True, max_length=100, null=True)

    def __str__(self):
        return str(self.tutoring_with)


class TutoringInLevel(models.Model):
    tutoring_in_level = models.CharField(unique=True, max_length=100, null=True)

    def __str__(self):
        return str(self.tutoring_in_level)

class PreferredCareerField(models.Model):
    preferred_career_field = models.CharField(unique=True, max_length=200, null=True)
    status = models.BooleanField(null=True, default=True)
    order_rank = models.PositiveIntegerField(null=True, default=0)

    def __str__(self):
        return str(self.preferred_career_field)

    class Meta:
        ordering = ['-order_rank']

class PreferredLocation(models.Model):
    preferred_location = models.CharField(unique=True, max_length=200, null=True)
    status = models.BooleanField(null=True, default=True)

    def __str__(self):
        return str(self.preferred_location)

    class Meta:
        ordering = ['preferred_location']

class SkillsToDevelop(models.Model):
    skills_to_develop = models.CharField(unique=True, max_length=200, null=True)
    status = models.BooleanField(null=True, default=True)

    def __str__(self):
        return str(self.skills_to_develop)

    class Meta:
        ordering = ['skills_to_develop']

class CustomUserPersonalInformation(models.Model):
    user_slug = models.CharField(unique=True, max_length=50, null=True)
    first_name = models.CharField(max_length=50, null=True)
    # middle_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=50, null=True)
    name_slug = models.SlugField(max_length=255, null=True)
    date_of_birth = models.DateField(null=True)
    gender = models.IntegerField(choices=gender_choices, null=True)
    country = CountryField(null=True)
    country_slug = models.SlugField(max_length=255, null=True)
    spoken_languages = models.ManyToManyField('SpokenLanguage')
    phone = models.CharField(max_length=20, null=True)
    currently_living_in = CountryField(null=True, blank_label='Select')
    currently_living_in_slug = models.SlugField(max_length=255, null=True)
    profile_pic = models.FileField(upload_to='user_profile/', null=True, validators=[validate_file_size])
    about_me = models.CharField(max_length=805, null=True, blank=True)
    hobbies = models.ManyToManyField('Hobby', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.first_name + '(' + self.user_slug + ')')

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.first_name)
        self.currently_living_in_slug = slugify(self.currently_living_in.name)
        self.country_slug = slugify(self.country.name)

        super(CustomUserPersonalInformation, self).save(*args, **kwargs)

    def calculate_age(self):
        today = datetime.date.today()
        if today and self.date_of_birth:
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            if age < 18:
                from django.utils.html import format_html
                return format_html("<span class='text-danger font-weight-bold'>" + str(age) + "</span>")
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        else:
            return ''

    class Meta:
        db_table = "users"
        verbose_name = 'custom_user_pi'
        verbose_name_plural = 'custom_users_pi'


class MentorPersonalInformation(models.Model):
    admin = models.OneToOneField(CustomUserPersonalInformation, on_delete=models.CASCADE, null=True)
    studying_in = CountryField(null=True)
    studying_in_slug = models.SlugField(max_length=255, null=True)
    currently_studying = models.IntegerField(null=True, choices=area_of_study_choice)
    currently_studying_slug = models.SlugField(max_length=255, null=True)
    passport = models.FileField(upload_to='mentor_passports/', null=True, validators=[validate_file_size] )
    phone = models.CharField(max_length=20, null=True)
    university_email = models.EmailField(null=True, blank=True)

    # Education Details
    are_you_graduated = models.IntegerField(null=True, choices=questions_choice, default=0)
    study_year = models.IntegerField(null=True, choices=STUDY_YEAR, blank=True)
    subject = models.IntegerField(null=True, choices=area_of_study_choice)
    name_of_school = models.CharField(max_length=50, null=True)

    # Foundation course
    did_you_study_the_foundation_course_in_uk = models.IntegerField(null=True, choices=questions_choice, blank=True)
    where_did_you_study = models.CharField(max_length=50, null=True, blank=True)
    subject_foundation = models.ManyToManyField('SubjectFoundation', blank=True)
    foundation_provider = models.CharField(max_length=50, null=True, blank=True)

    programme_level = models.IntegerField(null=True, choices=programme_level_choices_mentor, )
    UNIVERSITY_START_YEAR_CHOICES = [('', 'Select')]
    for r in range((datetime.datetime.now().year - 6), (datetime.datetime.now().year + 1)):
        UNIVERSITY_START_YEAR_CHOICES.append((r, r))
    university_start_year = models.IntegerField(choices=UNIVERSITY_START_YEAR_CHOICES, default=datetime.datetime.now().year,
                                         null=True,
                                         blank=True)
    YEAR_GRADUATED_CHOICES = [('', 'Select')]
    for r in range((datetime.datetime.now().year - 2), (datetime.datetime.now().year + 1)):
        YEAR_GRADUATED_CHOICES.append((r, r))
    year_graduated = models.IntegerField(choices=YEAR_GRADUATED_CHOICES, default=datetime.datetime.now().year,
                                         null=True,
                                         blank=True)
    student_id = models.FileField(upload_to='user_profile/', null=True, blank=True, validators=[validate_file_size])
    unibuddy = models.CharField(null=True, max_length=50, blank=True)

    # Previous Qualification
    previous_qualification = models.TextField(null=True, blank=True)

    # Advisory Experience
    are_you_registered_as_an_ambassador = models.IntegerField(null=True, choices=questions_choice)

    # Tutoring Experience
    are_you_currently_a_tutor = models.IntegerField(null=True, choices=questions_choice)
    platform_choice = (
        (0, 'Privately'),
        (1, 'Online Platform'),
    )
    do_you_tutor_privately_or_online = models.IntegerField(null=True, choices=platform_choice, blank=True)
    have_experience_tutoring_agency_or_online = models.IntegerField(null=True, blank=True, default=0, choices=questions_choice)
    name_of_agency_or_online_platforms = models.CharField(max_length=100, null=True, blank=True)
    hours_you_tutored = models.IntegerField(null=True, blank=True)
    hours_you_commit_to_tutor = models.IntegerField(null=True, blank=True)
    tutoring_subject = models.CharField(max_length=800, null=True, blank=True)
    tutoring_with = models.CharField(max_length=800, null=True, blank=True)
    tutoring_subject_list = models.ManyToManyField('TutoringSubject', blank=True)
    tutoring_with_list = models.ManyToManyField('TutoringWith', blank=True)
    languages_i_can_teach = models.ManyToManyField('SpokenLanguage', blank=True)

    tutoring_subject_other = models.CharField(max_length=255, null=True, blank=True)
    tutor_exp = models.CharField(max_length=50, null=True, blank=True)
    TUTORING_LEVEL = (
        ('Highschool', 'Highschool'),
        ('College / University', 'College / University'),
        ('English Language', 'English Language'),
    )
    tutoring_in_level = models.CharField(max_length=100, null=True, blank=True)
    tutoring_in_level_list = models.ManyToManyField('TutoringInLevel', blank=True)

    online_platform = models.CharField(null=True, max_length=100, blank=True)

    # About me
    write_something_about_you = models.CharField(max_length=200, null=True, blank=True)
    facebook_profile_url = models.CharField(null=True, max_length=200, blank=True)
    instagram_profile_url = models.CharField(null=True, max_length=200, blank=True)
    tiktok_profile_url = models.CharField(null=True, max_length=200, blank=True)
    twitter_profile_url = models.CharField(null=True, max_length=200, blank=True)
    linkedin_profile_url = models.CharField(null=True, max_length=200, blank=True)
    societies = models.CharField(max_length=100, null=True, blank=True)
    my_skills = models.CharField(max_length=100, null=True, blank=True)
    hobbies_and_interest = models.CharField(max_length=100, null=True, blank=True)

    # Content Creation
    experience_in_content_creation = models.IntegerField(null=True, choices=questions_choice)
    about_content_creation = models.TextField(null=True, blank=True)

    # Maximise your employability
    profile_made_visible_to_employers = models.IntegerField(null=True, choices=questions_choice)
    about_yourself = models.TextField(null=True, blank=True)
    cv = models.FileField(upload_to='documents/cv', blank=True, null=True, validators=[validate_file_size])
    preferred_career_field = models.ForeignKey(PreferredCareerField, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_location = models.ForeignKey(PreferredLocation, on_delete=models.SET_NULL, null=True, blank=True)
    skills_to_develop = models.ManyToManyField('SkillsToDevelop', blank=True)
    where_will_you_be_during_the_completion_of_your_internship = CountryField(null=True, blank=True)
    DURATION_OF_INTERNSHIP_TYPE = (
        ('', 'Select'),
        ('1 Month', '1 Month'),
        ('2 Months', '2 Months'),
        ('3 Months', '3 Months'),
        ('4 Months', '4 Months'),
    )
    duration_of_internship = models.CharField(max_length=50, choices=DURATION_OF_INTERNSHIP_TYPE, null=True, blank=True)
    WEEKLY_WORKING_HOURS_TYPE = (
        ('', 'Select'),
        ('2 Hours', '2 Hours'),
        ('5 Hours', '5 Hours'),
        ('10 Hours', '10 Hours'),
        ('15 Hours', '15 Hours'),
        ('20 Hours', '20 Hours'),
    )
    weekly_working_hours = models.CharField(max_length=50, choices=WEEKLY_WORKING_HOURS_TYPE, null=True, blank=True)
    would_you_like_us_to_generate_a_CV  = models.IntegerField(null=True, blank=True, default=0,
                                                                    choices=questions_choice)

    # DBS Information
    dbs_check = models.IntegerField(null=True, choices=questions_choice)
    DBS_CERTIFICATE_TYPE = (
        ('', 'Select'),
        (1, 'Type 1'),
        (2, 'Type 2'),
    )
    dbs_certificate_type = models.IntegerField(null=True, choices=DBS_CERTIFICATE_TYPE, blank=True)
    dbs_Reference_no = models.PositiveBigIntegerField(null=True, blank=True)
    dbs_date = models.DateField(null=True, blank=True)
    dbs_certificate = models.FileField(upload_to='documents/dbs_certificate', blank=True, null=True, validators=[validate_file_size])
    dbs_certificate_no = models.PositiveBigIntegerField(null=True, blank=True)
    dbs_declaration = models.TextField('Please state anything you wish to declare regarding your DBS',
                                       null=True, blank=True)

    # Social Media
    follow_us_on_facebook = models.BooleanField(null=True, )
    follow_us_on_instagram = models.BooleanField(null=True, )
    follow_us_on_tiktok = models.BooleanField(null=True, )
    follow_us_on_twitter = models.BooleanField(null=True, )
    follow_us_on_linkedin = models.BooleanField(null=True, )
    follow_us_on_youtube = models.BooleanField(null=True, )

    # Consents
    consent1 = models.BooleanField(null=True, )
    consent2 = models.BooleanField(null=True, )
    consent3 = models.BooleanField(null=True, )
    consent4 = models.BooleanField(null=True, )

    # Late-point
    late_point = models.URLField(null=True, max_length=100, blank=True)

    # Eligibility to work
    are_you_a_uk_national = models.BooleanField('Are you a UK national', default=False)
    tier_4_visa_allow_you_to_work_in_uk = models.BooleanField(('Does your Tier 4 Student Visa allow you to be '
                                                               'employed in the UK?'), default=False)
    visa_start_date = models.DateField(null=True, blank=True)
    visa_end_date = models.DateField(null=True, blank=True)
    visa_card = models.FileField(upload_to='documents/visa_card', blank=True, null=True, validators=[validate_file_size])
    eligible_to_work_in_country_living_in = models.BooleanField(default=False)
    brp_card = models.FileField(upload_to='documents/brp_card', blank=True, null=True, validators=[validate_file_size])

    # Mentor profile slug
    url_slug = models.SlugField(max_length=200, null=True, blank=True)

    # YouTube shots link
    youtube_shots = models.URLField(null=True, max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # Create slug for studying_in
        self.studying_in_slug = slugify(self.studying_in.name)
        # Create slug for currently_studying
        currently_studying = getsubject(self.currently_studying)
        self.currently_studying_slug = slugify(currently_studying)

        super(MentorPersonalInformation, self).save(*args, **kwargs)

    class Meta:
        db_table = "mentor_pi"


class StudentPersonalInformation(models.Model):
    admin = models.OneToOneField(CustomUserPersonalInformation, on_delete=models.CASCADE, null=True)
    media_consent = models.BooleanField(default=False)
    # education
    currently_studying = models.IntegerField(null=True, choices=questions_choice, default=0)
    current_or_last_school_name = models.CharField(max_length=200, null=True)
    study_destination = CountryField(multiple=True, blank=True, countries=DestinationCountries)
    
    student_id_card = models.FileField(upload_to='studentID/', null=True, blank=True, validators=[validate_file_size]) #New
    institute_email = models.EmailField(null=True, blank=True) #New

    # When do you hope to join us?
    area_of_study = models.PositiveIntegerField(null=True, choices=AP_COURSE)
    programme_level = models.IntegerField(null=True, choices=programme_level_choices_mentor)
    subject_foundation = models.ForeignKey('SubjectFoundation', on_delete= models.SET_NULL, null=True, blank=True) #New
    level_of_english = models.IntegerField(null=True, choices=level_of_english_choices)
    what_are_you_studying = models.CharField(max_length=100, null=True, blank=True)

    INTAKE_YEAR_CHOICES = [('', 'Select')]

    for r in range(2023, (datetime.datetime.now().year + 6)):
        INTAKE_YEAR_CHOICES.append((r, r))
    intake_year = models.IntegerField(choices=INTAKE_YEAR_CHOICES, null=True)
    last_qualification = models.CharField(max_length=100, null=True, blank=True)
    # About
    about_me = models.CharField(max_length=500, null=True, blank=True)
    consent1 = models.BooleanField(null=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.admin)

    class Meta:
        db_table = "student_pi"


class AppBasicInformation(models.Model):
    app = models.IntegerField(unique=True, null=True)
    user_slug = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=5, choices=TITLE_CHOICE, null=True)
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True)
    fullname = models.CharField(max_length=110, null=True)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(null=True)
    mobile = PhoneNumberField(null=True)
    phone = PhoneNumberField(null=True)
    mobile_number = models.CharField(max_length=20, null=True)
    nationality = CountryField(null=True, default='IN')
    gender = models.IntegerField(choices=gender_choices, null=True)
    native_languages = models.ManyToManyField('SpokenLanguage')
    MARITAL_STATUS = (
        ('', 'Select Marital Status'),
        ('0', 'Single'),
        ('1', 'Married'),
    )
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS, null=True)
    next_of_kin_name = models.CharField(max_length=50, null=True)
    relationship_to_student = models.CharField(max_length=50, null=True)
    next_of_kin_email = models.EmailField(null=True)
    next_of_kin_phone = PhoneNumberField(null=True, blank=True)

    # ========================== Student Fields ===============================
    media_consent = models.BooleanField(default=False)
    # Basic Information
    currently_living_in = CountryField(null=True, blank_label='Select')
    # Education
    currently_studying = models.IntegerField(null=True, choices=questions_choice, default=0)
    current_or_last_school_name = models.CharField(max_length=200, null=True)
    # study_destination = CountryField(multiple=True, blank=True, countries=DestinationCountries)
    # When do you hope to join us?
    # area_of_study = models.PositiveIntegerField(null=True, choices=area_of_study_choice)
    # programme_level = models.IntegerField(null=True, choices=programme_level_choices_mentor)
    level_of_english = models.IntegerField(null=True, choices=level_of_english_choices)
    what_are_you_studying = models.CharField(max_length=100, null=True, blank=True)
    # INTAKE_YEAR_CHOICES = [('', 'Select')]
    #
    # for r in range(2023, (datetime.datetime.now().year + 6)):
    #     INTAKE_YEAR_CHOICES.append((r, r))
    # intake_year = models.IntegerField(choices=INTAKE_YEAR_CHOICES, null=True)
    last_qualification = models.CharField(max_length=100, null=True, blank=True)
    # About
    about_me = models.CharField(max_length=500, null=True, blank=True)
    consent1 = models.BooleanField(null=True, )

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "basic_information"

    def __str__(self):
        return str(self.id)


class AppAddress(models.Model):
    app = models.OneToOneField(AppBasicInformation, on_delete=models.CASCADE, null=True, related_name='app_address')
    address_line_1 = models.CharField(max_length=50, null=True)
    address_line_2 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(null=True, max_length=20, blank=True)
    country = CountryField(null=True)

    class Meta:
        db_table = "app_address"

    def __str__(self):
        return str(self.id)


class AppPassportInformation(models.Model):
    app = models.OneToOneField(AppBasicInformation, on_delete=models.CASCADE, null=True,
                               related_name='app_passport_information')
    passport_number = models.CharField(max_length=10, null=True, unique=True)
    issue_date = models.DateField(null=True)
    expiry_date = models.DateField(null=True)
    issuing_authority = models.CharField(max_length=50, null=True)
    issuing_country = CountryField(null=True)
    place_of_birth = models.CharField(max_length=50, null=True)
    passport = models.FileField(upload_to='documents/', null=True, validators=[validate_file_size])

    class Meta:
        db_table = "app_passport_information"

    def __str__(self):
        return str(self.id)
