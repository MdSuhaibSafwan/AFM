import django_filters

from administration.models import CustomUser
from messaging.models import ReportUser
from django.db.models import Q

from personal_information.models import MentorPersonalInformation, CustomUserPersonalInformation


def filter_by_name(queryset, name, value):
    return queryset.filter(
        Q(reported_user__first_name__icontains=value) | Q(report_by_user__last_name__icontains=value))


class ReportUserFilter(django_filters.FilterSet):
    reported_user = django_filters.CharFilter(method='filter_by_name', label="Search user by name")
    report_by_user = django_filters.CharFilter(method='filter_by_name', label="Search reported by user by name")

    class Meta:
        model = ReportUser
        fields = ['reported_user', 'report_by_user']



class UserFilterByName(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method='filter_by_personal_information_name', label="Search by name")

    class Meta:
        model = CustomUser
        fields = ['keyword']

    def filter_by_personal_information_name(self, queryset, name, value):
        apps = CustomUserPersonalInformation.objects.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value))
        temp = []
        for i in apps:
            temp.append(i.user_slug)
        return queryset.filter(slug__in=temp)