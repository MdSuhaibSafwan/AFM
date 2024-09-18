import datetime
import pytz
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver

from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out

from django.utils.text import slugify
from personal_information.models import CustomUserPersonalInformation, StudentPersonalInformation, \
    MentorPersonalInformation, AppBasicInformation, AppAddress, \
    AppPassportInformation
from application.models import Application, EnglishLanguage, VisaHistory, PersonalStatement, Reference, \
    ProfessionalExperience, ProfessionalTrainingCertificate, AcademicQualification, ApplicationLog, \
    ApplicationAppliedAtUniversityLogin, ApplicationOfferStatus, ConsideredApplication, OmittedApp, \
    DirectApplication, ApplicationFeedback, \
    DocumentUpload

from phonenumber_field.modelfields import PhoneNumberField
from AFM.utils import unique_slug_generator
from django_countries.fields import CountryField
from notifications.signals import notify
from AFM.utils import get_current_request
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template import loader
import json
from AFM.validators import validate_file_size
TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

area_of_study_choice = (
    ('', 'Select'),
    (1, 'Business Studies'),
    (2, 'Social Studies'),
    (3, 'Arts & Design'),
    (4, 'Law'),
    (5, 'Biomedical Sciences'),
    (6, 'Medicine'),
    (7, 'Dentistry'),
    (8, 'pharmacy'),
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
)

level_of_english_choices = (
    (0, 'Beginner'),
    (1, 'Elementary'),
    (2, 'Pre-intermediate'),
    (3, 'Low Intermediate'),
    (4, 'Intermediate'),
    (5, 'Upper Intermediate'),
    (6, 'Pre-advanced'),
    (7, 'Advanced'),
    (8, 'Very Advanced'),
)

intake_month_choices = (
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

programme_level_choices_student = (
    (0, 'Foundation'),
    (1, 'Undergraduate'),
    (2, 'Postgraduate'),
    (3, 'Research'),
)
programme_level_choices_mentor = (
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

i_am_a_choose = (
    (1, 'Student'),
    (2, 'Parent'),
    (3, 'Mentor'),
    (4, 'University'),
    (5, 'College'),
)
Gender = (('', 'Select'), ('Male', 'Male'), ('Female', 'Female'), ('Prefer not to say', 'Prefer not to say'))

user_type_data = (
        ('', 'select-user'),
        (0, 'Super admin'),
        (1, 'Admin'),
        (2, 'Institute'),
        (3, 'Student'),
        (4, 'Mentor'),
        (5, 'Parent'),
        (6, 'Institute admin'),
        (7, 'App admin'),
        (8, 'Recruiter'),
        (9, 'System Mentor'),
        (10, 'System Recruiter'),
        (11, 'School'),
        (12, 'Future Student'),
    )

class CustomUser(AbstractUser):
    slug = models.CharField(null=True, unique=True, max_length=50, )
    user_type = models.PositiveIntegerField(choices=user_type_data, null=True)
    profile_pic = models.FileField(upload_to='user_profile/', blank=True, validators=[validate_file_size])
    how_did_you_hear_about_us = models.CharField(null=True, max_length=100, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    age = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(13)])
    timezone = models.CharField(max_length=32, choices=TIMEZONES,
                                default='UTC', null=False, blank=False)



    def __str__(self):
        return str(self.username) + ' (' + str(self.user_type) + ')'

    class Meta:
        db_table = "all_users"

    def my_name(self):
        # return self.first_name.capitalize() + ' ' + self.last_name.capitalize()
        if self.user_type == 4:
            mentor_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            return mentor_info.admin.first_name.capitalize()
        elif self.user_type == 3:
            student_info = AppBasicInformation.objects.using('afm_personal_information').get(
                user_slug=self.slug)
            return student_info.first_name.capitalize() + ' ' + student_info.surname.capitalize()
        else:
            return self.first_name.capitalize() + ' ' + self.last_name.capitalize()

    def get_first_name(self):
        if self.user_type == 4:
            mentor_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            return mentor_info.admin.first_name.capitalize()
        elif self.user_type == 3:
            student_info = AppBasicInformation.objects.using('afm_personal_information').get(
                user_slug=self.slug)
            return student_info.first_name.capitalize()
        else:
            return self.first_name.capitalize()

    def get_last_name(self):
        if self.user_type == 4:
            mentor_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            return mentor_info.admin.last_name.capitalize()
        elif self.user_type == 3:
            student_info = AppBasicInformation.objects.using('afm_personal_information').get(
                user_slug=self.slug)
            return student_info.surname.capitalize()
        else:
            return self.last_name.capitalize()

    class Meta:
        verbose_name = 'custom_user'
        verbose_name_plural = 'custom_users'

    # def my_unread_messages(self):
    #     request = get_current_request()
    #     return self.from_user.filter(read=False, recipient=request.user).count()
    @property
    def my_unread_messages(self):
        request = get_current_request()
        return self.message_sender.filter(read=False, receiver=request.user).count()
        # return Messaging.objects.filter(receiver=request.user, sender=self.sender).count()

    def personal_info_country(self):
        if self.user_type == 3:
            personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            str = "<span class='country-flags'> <i data-feather='map-pin'></i>" + personal_info.admin.country.name + "<img src=" + personal_info.admin.country.flag + " alt=''> </span>"

            return str
        return ''

    def personal_info_subject(self):
        if self.user_type == 3:
            try:
                # personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
                #     admin__user_slug=self.slug)
                # return personal_info.area_of_study
                return Application.objects.filter(admin__slug=self.slug).first().subject
            except:
                return ''
        return ''

    def personal_info_birthdate(self):
        if self.user_type == 3:
            personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            today = datetime.date.today()

            born = personal_info.admin.date_of_birth
            if born:
                return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return ''

    def personal_info_intake_year(self):
        if self.user_type == 3:
            personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            return personal_info.intake_year
        return ''

    def personal_info_last_qualification(self):
        if self.user_type == 3:
            personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            return personal_info.last_qualification

        return ''

    def personal_info_currently_studying(self):
        if self.user_type == 3:
            personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            return personal_info.currently_studying
        return ''

    def personal_info_what_are_you_studying(self):
        if self.user_type == 3:
            personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            return personal_info.what_are_you_studying
        return ''

    def mentor_university(self):
        if self.user_type == 4:
            print('Alumni ID', self.id)
            mentor_info = Mentor.objects.get(admin__slug=self.slug)
            if mentor_info.institute:
                print(mentor_info)
                return mentor_info.institute.institute_name
            else:
                return mentor_info.institute_name
        return ''

    def mentor_country(self):
        if self.user_type == 4:
            mentor_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            str = "<span class='country-flags'> <i data-feather='map-pin'></i>" + mentor_info.admin.country.name + "<img src=" + mentor_info.admin.country.flag + " alt=''> </span>"
            return str
        return ''

    def mentor_country_studying_in(self):
        if self.user_type == 4:
            mentor_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            str = "<span class='country-flags'> <i data-feather='map-pin'></i>" + mentor_info.studying_in.name + "<img src=" + mentor_info.studying_in.flag + " alt=''> </span>"
            return str
        return ''

    def mentor_late_point(self):
        link = '#'
        if self.user_type == 4:
            mentor_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=self.slug)
            if mentor_info.late_point:
                link = mentor_info.late_point
        return link

    def mentor_subject(self):
        if self.user_type == 4:
            try:
                mentor_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
                    admin__user_slug=self.slug)
                return mentor_info.currently_studying
            except:
                return ''
        return ''


class LoggedUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    online_status = models.BooleanField(null=True, blank=True, default=False)
    last_seen = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.user.username

    def login_user(sender, request, user, **kwargs):
        print("USER - ", user)
        loggeduser,created = LoggedUser.objects.update_or_create(user=user)
        loggeduser.online_status=True
        loggeduser.save()
        print("-------------------------Login Signal------------------------")
        print("Logged user, created - ", loggeduser, created)
        print("Logged User online status - ", loggeduser.online_status)
        print("User Logged in successfully.....")
        print("-------------------------Login Signal------------------------")


    def logout_user(sender, request, user, **kwargs):
        print("USER - ", user)
        loggeduser,created = LoggedUser.objects.update_or_create(user=user)
        loggeduser.online_status=False
        loggeduser.save()
        print("-------------------------Logout Signal------------------------")
        print("Logged user, created - ", loggeduser, created) 
        print("Logged User online status - ", loggeduser.online_status) 
        print("User Logged out successfully.....")   
        print("-------------------------Logout Signal------------------------")     

    user_logged_in.connect(login_user)
    user_logged_out.connect(logout_user)





class Admin(models.Model):
    meeting_link = models.URLField(max_length=200, null=True, blank=True)
    appointment_link = models.URLField(max_length=200, null=True, blank=True)


class Institute(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    institute_name = models.CharField(max_length=100, null=True, unique=True)
    institute_logo = models.ImageField(upload_to='institute_logo/', null=True, blank=True, validators=[validate_file_size])
    country = CountryField(null=True)
    institute_slug = models.SlugField(max_length=255, null=True, unique=True)
    # Institute account type 1. free account or 2.premium account
    account_type = models.BooleanField(default=False)

    # Scholarship fields
    funding_last_year = models.CharField(max_length=50, null=True, blank=True)
    funding_current_year = models.CharField(max_length=50, null=True, blank=True)
    # subject_and_programme_level = models.CharField(max_length=50, null=True, blank=True)
    countries_available = CountryField(multiple=True, blank=True)
    extra_notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.institute_slug = slugify(self.institute_name)
        super(Institute, self).save(*args, **kwargs)

    def __str__(self):
        return str(str(self.institute_name))

    class Meta:
        db_table = "institute"


class InstituteScholarshipProgramme(models.Model):
    subject = models.IntegerField(null=True, choices=area_of_study_choice, blank=True)
    programme_level = models.IntegerField(null=True, choices=programme_level_choices_student, blank=True)


class InstituteLead(models.Model):
    first_name = models.CharField(max_length=30, null=True, )
    last_name = models.CharField(max_length=30, null=True)
    ARE_YOU_CHOICES = (
        ('', 'Select'),
        (1, 'Institute'),
        (2, 'University')
    )
    are_you = models.IntegerField(choices=ARE_YOU_CHOICES, null=True)
    phone_no = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=50, null=True)
    message = models.TextField(null=True)


class InstituteAdmin(models.Model):
    ROLE = (
        ('Institution Staff', 'Institution Staff'),
        ('Ambassador', 'Ambassador'),
        ('Mentor', 'Mentor')
    )
    please_select_role = models.CharField(choices=ROLE, max_length=20, null=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(str(self.admin.first_name))

    class Meta:
        db_table = "institute_admin"


class School(models.Model):
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.SET_NULL, related_name='school')
    school_name = models.CharField(max_length=200, null=True, blank=True)
    school_logo = models.FileField(upload_to='school_logo/', null=True, blank=True,
                                      validators=[validate_file_size])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.admin.username)

    class Meta:
        db_table = "School"


class Mentor(models.Model):
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.SET_NULL)
    institute = models.ForeignKey(Institute, on_delete=models.SET_NULL, null=True, blank=True)
    institute_name = models.CharField(max_length=200, null=True, blank=True)
    institute_name_slug = models.SlugField(max_length=255, null=True, blank=True)
    institute_logo = models.FileField(upload_to='institute_logo/', null=True, blank=True, validators=[validate_file_size])
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    # Country select
    # currently_study_in = models.CharField(max_length=50, null=True)
    book_appointment_link = models.URLField(max_length=200, null=True, blank=True)
    # Mentor's Profile status : approved | rejected | hold
    profile_status = models.BooleanField(null=True, default=False)

    # Additional Question
    q1 = models.TextField(null=True, blank=True)
    q2 = models.TextField(null=True, blank=True)
    q3 = models.TextField(null=True, blank=True)
    q4 = models.TextField(null=True, blank=True)
    q5 = models.TextField(null=True, blank=True)
    q6 = models.TextField(null=True, blank=True)
    q7 = models.TextField(null=True, blank=True)
    q8 = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.admin.first_name)

    def save(self, *args, **kwargs):
        self.institute_name_slug = slugify(self.institute_name)
        super(Mentor, self).save(*args, **kwargs)

    class Meta:
        db_table = "mentor"


class Subscriber(models.Model):
    subscribe_to = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='subscriber')
    email = models.EmailField(max_length=100, null=True)


class Student(models.Model):
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.SET_NULL, related_name='student')
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    are_you_studying_an_online_course = models.IntegerField(null=True, choices=questions_choice)
    currently_studying_course = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    mentor = models.ManyToManyField('Mentor', blank=True)

    profile_status = models.BooleanField(null=True, default=False)

    # Additional Question
    q1 = models.TextField(null=True)
    q2 = models.TextField(null=True)
    q3 = models.TextField(null=True)
    q4 = models.TextField(null=True)
    q5 = models.TextField(null=True)
    q6 = models.TextField(null=True)

    def __str__(self):
        return str(self.admin.username)

    class Meta:
        db_table = "student"


class FutureStudent(models.Model):
    admin = models.OneToOneField(CustomUser, null=True, on_delete=models.SET_NULL, related_name='future_student')
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True)
    have_you_already_applied_to_this_school = models.IntegerField(null=True, choices=questions_choice)
    where_are_you_from = CountryField(null=True, blank_label='Select')
    YEAR_CHOICES = [('', 'Select')]
    for r in range(datetime.datetime.now().year, (datetime.datetime.now().year + 10)):
        YEAR_CHOICES.append((r, r))

    intake_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year, null=True)
    DESIRED_MONTH_CHOICES = (
        ('', 'Select'),
        (0, 'January'),
        (8, 'September'),
    )
    intake_month = models.PositiveIntegerField(null=True, choices=DESIRED_MONTH_CHOICES, default=8)
    course_you_interested_in = models.CharField(max_length=200, null=True)
    program_level = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.admin.username)

    class Meta:
        db_table = "future_student"


class AdditionalQuestions(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, related_name='additional_questions')
    q1 = models.TextField(null=True)


class MentorFeedback(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True)
    admin = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    feedback = models.CharField(max_length=50, null=True)
    q1 = models.CharField(max_length=10, null=True)
    q2 = models.CharField(max_length=10, null=True)
    q3 = models.IntegerField(null=True, choices=questions_choice)
    q4 = models.IntegerField(null=True, choices=questions_choice)
    status = models.BooleanField(null=True, default=False)

    class Meta:
        db_table = "mentor_feedback"


class AfmLinkUser(models.Model):
    admin = models.ForeignKey(Institute, null=True, on_delete=models.CASCADE)
    institute_slug = models.CharField(null=True, max_length=50)

    def __str__(self):
        return str(self.admin)

    class Meta:
        db_table = "afm_links_users"


class Recruiter(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True, )
    WORK_TYPE = (
        ('', '-- Select Work Type --'),
        (1, 'Company'),
        (2, 'Individual'),
        (3, 'School'),
    )
    gender = models.CharField(choices=Gender, null=True, max_length=20)
    profile_pic = models.FileField(upload_to='user_profile/', null=True, blank=True, validators=[validate_file_size])
    date_of_birth = models.DateField(null=True)
    country = CountryField(blank=True)
    phone_no = PhoneNumberField(null=True)
    status = models.IntegerField(choices=profile_status_choices, null=True)
    work_type = models.CharField(choices=WORK_TYPE, null=True, max_length=5)
    company_name = models.CharField(max_length=110, null=True, blank=True)
    company_website = models.URLField(max_length=200, null=True, blank=True)
    countries_recruit_from = CountryField(multiple=True, blank=True)
    countries_recruit_to = CountryField(multiple=True, blank=True)
    passport = models.FileField(null=True, blank=True, upload_to='recruiters/passports/', validators=[validate_file_size])
    registration_certificate = models.FileField(null=True, blank=True, upload_to='recruiters/registration_certificate/', validators=[validate_file_size])
    bank_name = models.CharField(max_length=110, null=True, blank=True)
    account_name = models.CharField(max_length=110, null=True, blank=True)
    sort_code = models.CharField(max_length=15, null=True, blank=True)
    account_number = models.CharField(max_length=40, null=True, blank=True)
    iban = models.CharField(max_length=40, null=True, blank=True)
    swit = models.CharField(max_length=15, null=True, blank=True)
    ifsc = models.CharField(max_length=15, null=True, blank=True)
    bank_address = models.CharField(max_length=110, null=True, blank=True)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
    county = models.CharField(max_length=50, blank=True, null=True)
    postcode = models.CharField(max_length=10, null=True, blank=True)
    about_me = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.admin)

    class Meta:
        db_table = "recruiters"

    class Meta:
        verbose_name = 'recruiter'
        verbose_name_plural = 'recruiters'


class Lead(models.Model):
    slug = models.CharField(null=True, unique=True, max_length=50, )

    admin = models.ForeignKey(Recruiter, null=True, on_delete=models.SET_NULL, blank=True)
    app = models.ForeignKey(Application, null=True, on_delete=models.CASCADE, blank=True)

    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    phone_no = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=50, null=True)
    subject_interest = models.IntegerField(null=True, choices=area_of_study_choice)
    interested_in_academic_counselling = models.IntegerField(null=True, choices=questions_choice)
    INTAKE_YEAR_CHOICES = [('', 'Select')]

    for r in range((datetime.datetime.now().year + 2), datetime.datetime.now().year):
        INTAKE_YEAR_CHOICES.append((r, r))
    intake_year = models.IntegerField(choices=INTAKE_YEAR_CHOICES, default=datetime.datetime.now().year, null=True)
    country = CountryField(blank=True)
    where_did_you_hear_about_us = models.CharField(max_length=50, null=True)
    message = models.CharField(max_length=200, null=True)
    take_lead = models.BooleanField(null=True, default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.admin)

    class Meta:
        db_table = "Lead"


class InstituteRecruiterWorkWith(models.Model):
    admin = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    # institute = models.ManyToManyField(Institute)
    institute = models.ForeignKey(Institute, null=True, on_delete=models.CASCADE, blank=True)
    institute_name = models.CharField(max_length=50, null=True, blank=True)
    country_name = CountryField(null=True)
    # agreement_start_date = models.DateField(null=True)
    # agreement_end_date = models.DateField(null=True)
    YEAR_CHOICES = [('', 'Select')]
    for r in range(datetime.datetime.now().year, (datetime.datetime.now().year + 2)):
        YEAR_CHOICES.append((r, r))

    agreement_start_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year, null=True)
    agreement_start_month = models.PositiveIntegerField(null=True, choices=intake_month_choices)
    agreement_end_year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year, null=True)
    agreement_end_month = models.PositiveIntegerField(null=True, choices=intake_month_choices)

    agreement_doc = models.FileField(null=True, blank=True, validators=[validate_file_size])
    # #new
    # students_last_year = models.PositiveIntegerField(null=True, blank=True)
    # students_this_year = models.PositiveIntegerField(null=True, blank=True)
    # email = models.EmailField(max_length=50, null=True,  blank=True)
    # phone_no = PhoneNumberField(null=True, blank=True)

    students_last_year = models.PositiveIntegerField(null=True, blank=True)
    students_this_year = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    contact_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.admin)


class Parent(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    mentor = models.ManyToManyField('Mentor')
    phone_no = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=400, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(null=True, max_length=20, blank=True)
    country = CountryField(null=True, )

    def __str__(self):
        return str(self.admin)

    class Meta:
        db_table = "parent"


class AppAdmin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.admin)

    class Meta:
        db_table = "app admin"


class ContactUs(models.Model):
    admin = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    country = CountryField(null=True)
    i_am_a = models.IntegerField(null=True, choices=i_am_a_choose)
    connect_with_a_mentor = models.IntegerField(null=True, choices=questions_choice)
    name = models.CharField(null=True, max_length=110)
    email = models.EmailField(null=True, max_length=50)
    phone_no = PhoneNumberField(null=True, blank=True)
    subject = models.CharField(null=True, max_length=110)
    message = models.TextField(null=True)
    question1 = models.IntegerField(null=True, choices=questions_choice)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "contact_us"

    def __str__(self):
        return str(self.name)


class TechSupport(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
    subject = models.CharField(null=True, max_length=110)
    message = models.TextField(null=True)

    class Meta:
        db_table = "tech_support"


class BlockUser(models.Model):
    reported_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='reported_user')
    report_by_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='reported_by')
    user_assigned = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name='user_assigned')
    message = models.TextField(null=True)
    screenshot = models.FileField(null=True, blank=True, validators=[validate_file_size])
    is_removed = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

AGE = (
    ('', 'Select'),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
    ("16", "16"),
    ("17", "17"),
    ("18", "18"),
    ("19", "19"),
    ("20", "20"),
    ("21", "21"),
    ("22", "22"),
    ("23+", "23+"),
    ("I'm a Parent/Guardian", "I'm a Parent/Guardian"),
)

REASONE_FOR_AN_APPOINTMENT = (
    ('', 'Select'),
    ("Choosing a University", "Choosing a University"),
    ("University Application", "University Application"),
    ("Study Experience", "Study Experience"),
    ("Tutoring", "Tutoring"),
    ("Exam Preparation", "Exam Preparation"),
    ("Employment Prospects", "Employment Prospects"),
    ("Other", "Other"),
)

A_AM = (
    ('', 'Select'),
    ("the Applicant", "the Applicant"),
    ("a Parent", "a Parent"),
    ("a School", "a School"),
    ("an Agent", "an Agent"),
)


class MentorBookingLeads(models.Model):
    mentor = models.ForeignKey(Mentor, null=True, on_delete=models.CASCADE)
    date_for_appointment = models.DateField(null=True)
    time_for_appointment = models.TimeField(null=True)
    first_name = models.CharField(null=True, max_length=110)
    last_name = models.CharField(null=True, max_length=110)
    email = models.EmailField(null=True, max_length=50)
    i_am = models.CharField(max_length=100, null=True, choices=A_AM)
    age_of_applicant = models.CharField(max_length=40, null=True, choices=AGE)
    country = CountryField(null=True)
    reasone_for_an_appointment = models.CharField(max_length=100, null=True, choices=REASONE_FOR_AN_APPOINTMENT)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


SUBJECT = (
    ('', 'Select'),
    (1, 'Business Studies'),
    (2, 'Social Studies'),
    (3, 'Arts & Design'),
    (4, 'Law'),
    (5, 'Biomedical Sciences'),
    (6, 'Medicine'),
    (7, 'Dentistry'),
    (8, 'pharmacy'),
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
)


class DemandAndSupply(models.Model):
    spoken_language = models.CharField(null=True, max_length=100)
    country = CountryField(null=True)
    subject = models.PositiveIntegerField(null=True, choices=SUBJECT)
    demand = models.CharField(null=True, max_length=100)
    supply = models.CharField(null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class MentorPublicProfileComment(models.Model):
    COMMENT_STATUS = (
        (True, 'published'),
        (False, 'draft'),
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='receiver')
    comment = models.TextField(null=True)
    comment_status = models.BooleanField(null=True, choices=COMMENT_STATUS, default=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE,)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = "mentor_public_profile_comments"


# class DeletedUserData(models.Model):
#     slug = models.CharField(null=True, unique=True, max_length=50, )
#     user_type = models.PositiveIntegerField(choices=user_type_data, null=True)

class UserCSVImportedData(models.Model):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    user_type = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True, max_length=100)
    date_of_birth = models.DateField(null=True)
    nationality = CountryField(null=True)
    currently_studying_course = models.CharField(max_length=100, null=True)
    languages = models.CharField(max_length=200, null=True)
    year_left = models.CharField(max_length=10, null=True)
    course_studied = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True)
    is_imported = models.BooleanField(default=False)

    class Meta:
        db_table = "user_csv_imported_data"