import django_filters
from page.models import Page

class PageFilter(django_filters.FilterSet):

    class Meta:
        model = Page
        fields = ['post_status']
