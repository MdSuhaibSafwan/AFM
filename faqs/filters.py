from faqs.models import Faq
import django_filters
class FaqFilter(django_filters.FilterSet):
    class Meta:
        model = Faq
        fields = ['user_type',]