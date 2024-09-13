import django_countries
import django_filters
from administration.models import Recruiter, MentorFeedback, CustomUser, Parent, MentorBookingLeads, DemandAndSupply, \
    TechSupport, ContactUs, Mentor, Institute
from personal_information.models import MentorPersonalInformation, SpokenLanguage, StudentPersonalInformation
from django import forms
from django_countries import countries
from django.db.models import Q


class DateInput(forms.DateInput):
    input_type = 'date'


class DemandAndSupplyFilter(django_filters.FilterSet):
    SUBJECT = (
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
    subject = django_filters.ChoiceFilter(choices=SUBJECT, empty_label='Select')
    COUNTRY = []
    for i in DemandAndSupply.objects.all().distinct('country').order_by('country'):
        country_data = (i.country, i.country.name)
        COUNTRY.append(country_data)

    country = django_filters.ChoiceFilter(choices=COUNTRY, empty_label='Select')
    LANGUAGES = []

    for i in DemandAndSupply.objects.all().distinct('spoken_language').order_by('spoken_language'):
        language_data = (i.spoken_language, i.spoken_language)
        LANGUAGES.append(language_data)

    spoken_language = django_filters.ChoiceFilter(choices=LANGUAGES, empty_label='Select')

    class Meta:
        model = DemandAndSupply
        fields = ('spoken_language', 'country', 'subject',)




class MentorBookingLeadsFilter(django_filters.FilterSet):
    REASONE_FOR_AN_APPOINTMENT = (
        ("Choosing a University", "Choosing a University"),
        ("University Application", "University Application"),
        ("Study Experience", "Study Experience"),
        ("Tutoring", "Tutoring"),
        ("Exam Preparation", "Exam Preparation"),
        ("Employment Prospects", "Employment Prospects"),
        ("Other", "Other"),
    )
    reasone_for_an_appointment = django_filters.ChoiceFilter(choices=REASONE_FOR_AN_APPOINTMENT, empty_label='Select')
    # date_for_appointment = django_filters.DateFilter(widget=DateInput())
    email = django_filters.CharFilter(method='filter_by_email', label="Search by email")

    class Meta:
        model = MentorBookingLeads
        fields = ['mentor', 'email', 'country', 'reasone_for_an_appointment']

    def filter_by_email(self, queryset, name, value):
        queryset = queryset.filter(email__icontains=value)
        return queryset


class MentorFilter(django_filters.FilterSet):
    # available_from = django_filters.DateFilter(widget=DateInput(), method='filter_by_available_date')
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
    )
    programme_level_choices_mentor = (
        ('', 'Select'),
        (0, 'Foundation'),
        (1, 'Undergraduate'),
        (2, 'Postgraduate'),
        (3, 'Research'),
    )
    COUNTRY_CHOICES = (
        ('IN', 'India'),
        ('GB', 'United Kingdom'),
        ('US', 'United States of America'),
    )
    LANGUAGES = (
        ('Hindi', 'Hindi'),
        ('English', 'English'),
    )
    QUESTION_CHOICE = (
        (0, 'Mentor'),
        (1, 'Alumni'),
    )
    MENTOR_PROFILE_STATUS_CHOICES = (
        ('Incomplete', 'Incomplete'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
    )

    # spoken_languages = django_filters.ModelMultipleChoiceFilter(queryset=SpokenLanguage.objects.all(),
    #                                                             label="Spoken Languages"
    #                                                     )
    are_you_graduated = django_filters.ChoiceFilter(choices=QUESTION_CHOICE, empty_label='Select Mentor',
                                                    )
    studying_in_countries = django_filters.MultipleChoiceFilter(
        choices=countries, method='filter_countries', label="Mentors currently studying in")
    currently_studying = django_filters.ChoiceFilter(choices=area_of_study_choice, empty_label='Area of Study')
    keyword = django_filters.CharFilter(method='filter_by_name', label="Search by keyword")
    email = django_filters.CharFilter(method='filter_by_email', label="Search by email")
    mentor_profile_status = django_filters.ChoiceFilter(choices=MENTOR_PROFILE_STATUS_CHOICES,
                                                        empty_label='Select status',
                                                        method='filter_by_mentor_profile_status',)
    # institute = django_filters.ModelChoiceFilter(field_name='institute_name', queryset=Institute.objects.all(), method='filter_by_institute',
    #                                              label="Select Institute", empty_label='Select Institute',)

    class Meta:
        model = MentorPersonalInformation
        fields = ['programme_level', 'currently_studying', 'admin__country', 'studying_in', 'admin__spoken_languages',
                  'are_you_graduated', 'mentor_profile_status', ]

    def __init__(self, *args, **kwargs):
        super(MentorFilter, self).__init__(*args, **kwargs)
        self.filters['admin__spoken_languages'].label = "Languages they speak"
        self.filters['admin__country'].label = "Mentors originally from"
        self.filters[
            'admin__spoken_languages'].help_text = "<span>You can view the current exchange rate on : <a href='https://xe.com/' target='_blank'>xe.com</a></span>"

        # self.filters['currently_studying'].label = "Area of Study"

    def filter_spoken_languages(self, queryset, name, value):
        # value should be a list since it's multiple choice
        # queryset = Mentor_PI.objects.filter(admin__spoken_languages__in = value)
        # return queryset
        return queryset.filter(**{
            'admin__spoken_languages__language__in': value,
        })

    def filter_countries(self, queryset, name, value):
        return queryset.filter(**{
            'studying_in__in': value,
        })

    def filter_currently_studying(self, queryset, name, value):
        return queryset.filter(**{
            'currently_studying__in': value,
        })

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(Q(admin__first_name__icontains=value) | Q(admin__first_name__icontains=value))

    def filter_by_email(self, queryset, name, value):
        apps = CustomUser.objects.filter(email__icontains=value)
        temp = []
        for i in apps:
            temp.append(i.slug)
        return queryset.filter(admin__user_slug__in=temp)

    def filter_by_mentor_profile_status(self, queryset, name, value):
        if value == 'Incomplete':
            return queryset.filter(Q(consent4=None) | Q(consent4=False))
        elif value == 'Pending':
            apps = Mentor.objects.filter(profile_status=False)
            temp = []
            for i in apps:
                temp.append(i.admin.slug)
            return queryset.filter(admin__user_slug__in=temp, consent4=True)
        elif value == 'Approved':
            apps = Mentor.objects.filter(profile_status=True)
            temp = []
            for i in apps:
                temp.append(i.admin.slug)
            return queryset.filter(admin__user_slug__in=temp)
        return queryset



class RecruiterFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(method='filter_by_email', label="Search by email")

    class Meta:
        model = Recruiter
        fields = ['work_type']

    def filter_by_email(self, queryset, name, value):
        return queryset.filter(admin__email__icontains=value)


class StudentFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_by_name', label="Search by name")
    email = django_filters.CharFilter(method='filter_by_email', label="Search by email")

    class Meta:
        model = StudentPersonalInformation
        fields = ['keyword']

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(Q(admin__first_name__icontains=value) | Q(admin__last_name__icontains=value))

    def filter_by_email(self, queryset, name, value):
        apps = CustomUser.objects.filter(email__icontains=value)
        temp = []
        for i in apps:
            temp.append(i.slug)
        return queryset.filter(admin__user_slug__in=temp)


class TestimonialsFilter(django_filters.FilterSet):
    class Meta:
        model = MentorFeedback
        fields = ['mentor', 'admin']


class ParentFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_by_name', label="Search by name")
    email = django_filters.CharFilter(method='filter_by_email', label="Search by email")

    class Meta:
        model = Parent
        fields = ['keyword', 'email']

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(Q(admin__first_name__icontains=value) | Q(admin__last_name__icontains=value))

    def filter_by_email(self, queryset, name, value):
        return queryset.filter(admin__email__icontains=value)


class TechSupportFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_by_name', label="Search by name")
    email = django_filters.CharFilter(method='filter_by_email', label="Search by email")

    class Meta:
        model = TechSupport
        fields = ['keyword', 'email', 'user__user_type']

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(Q(user__first_name__icontains=value) | Q(user__last_name__icontains=value))

    def filter_by_email(self, queryset, name, value):
        return queryset.filter(user__email__icontains=value)


class ContactUsFilter(django_filters.FilterSet):
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'i_am_a', 'country']