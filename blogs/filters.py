import django_filters

from administration.models import Recruiter
from blogs.models import Post
from personal_information.models import MentorPersonalInformation, SpokenLanguage
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'


class BlogFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = ['author', 'status']

