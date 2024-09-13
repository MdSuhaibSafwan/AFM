from datetime import datetime

import django_filters
from application.models import Application
from django import forms
from django_countries.fields import CountryField
from personal_information.models import AppBasicInformation


class DateInput(forms.DateInput):
    input_type = 'date'


class ApplicationFilter(django_filters.FilterSet):
    YEAR_CHOICES = [('', 'Select')]
    for r in range(datetime.now().year, (datetime.now().year + 20)):
        YEAR_CHOICES.append((r, r))

    programme_level_choices_student = (
        ('', 'Select'),
        (0, 'Foundation'),
        (1, 'Undergraduate'),
        (2, 'Postgraduate'),
        (3, 'Research'),
    )

    area_of_study_choice = (
        (6, 'Medicine'),
    )
    COUNTRY_CHOICES = (
        ('GB', 'United Kingdom'),
        ('IE', 'Ireland'),
        ('US', 'United States of America'),
        ('CA', 'Canada'),
        ('AU', 'Australia'),
        ('NZ', 'New Zealand'),

        ('IN', 'India'),
        ('HU', 'Hungary'),
        ('HR', 'Croatia'),
        ('GE', 'Germany'),
        ('IT', 'Italy'),
        ('RU', 'Russia'),
        ('SG', 'Singapore'),
        ('SK', 'Slovakia'),
        ('GD', 'Grenada'),
        ('CZ', 'Czechia'),
        ('PL', 'Poland'),
        ('ES', 'Spain'),

        ('BS', 'Bahamas'),
        ('KY', 'Cayman Islands'),
        ('TC', 'Turks and Caicos Islands'),
        ('AE', 'United Arab Emirates'),
        ('VG', 'Virgin Islands (British)'),
        ('VI', 'Virgin Islands (U.S.)'),
        ('NL', 'Netherlands'),
    )
    study_destination_country = django_filters.ChoiceFilter(choices=COUNTRY_CHOICES, empty_label='Country')
    # country = CountryField().formfield()
    intake_year = django_filters.ChoiceFilter(choices=YEAR_CHOICES, empty_label='Intake Year')
    program_level = django_filters.ChoiceFilter(choices=programme_level_choices_student, empty_label='Programme Level')
    subject = django_filters.ChoiceFilter(choices=area_of_study_choice, empty_label='Subject')

    class Meta:
        model = Application
        fields = ['study_destination_country', 'intake_year', 'program_level', 'subject']

    # def filter_by_available_date(self, queryset, name, value):
    #     return queryset.filter(available_from__gt=value)

    # def filter_by_country(self, queryset, name, value):
    #     apps = App_Basic_Information.objects.using('afm_personal_information').filter(nationality=value)
    #     temp = []
    #     for i in apps:
    #         temp.append(i.id)
    #     return queryset.filter(id__in=temp)
