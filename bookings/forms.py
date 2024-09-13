from django import forms
from administration.models import CustomUser
from bookings.models import Services, UserServices, Appointment
from django_summernote.widgets import SummernoteWidget


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['title', 'description']

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control shadow ', }
        self.fields['description'].widget = SummernoteWidget()
        # self.fields['duration'].widget.attrs = {'class': 'form-control shadow ', 'placeholder': 'HH:MM:SS eg: 00:15:20'}
        # self.fields['price'].widget.attrs = {'class': 'form-control shadow ', }


class ServiceUpdateForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['title', 'description', 'duration', 'is_active', ]

    def __init__(self, *args, **kwargs):
        super(ServiceUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'class': 'form-control shadow ', }
        self.fields['description'].widget = SummernoteWidget()
        self.fields['duration'].widget.attrs = {'class': 'form-control shadow ', 'placeholder': 'HH:MM:SS eg: 00:15:20'}


class UserServicesForm(forms.ModelForm):
    class Meta:
        model = UserServices
        fields = ('service', )

    widgets = {
        'service': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Service','required': 'True'}),
    }

    # def __init__(self, *args, **kwargs):
    #     super(UserServicesForm, self).__init__(*args, **kwargs)
    #     self.fields['service'].widget.attrs = {'class': 'form-control shadow select'}
    #     # self.fields['price'].widget.attrs = {'class': 'form-control shadow'}


class AdminAppointmentForm(forms.ModelForm):
    provider_id = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type=4))
    provider = forms.CharField(max_length=512)
    # booker = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type=3))
    services = forms.ModelChoiceField(queryset=Services.objects.all())
    date = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(attrs={
            'class': 'form-control shadow',
            'data-target': '#id_date'
        })
    )
    time = forms.CharField(
        widget=forms.RadioSelect
    )

    class Meta:
        model = Appointment
        fields = ('provider', 'booker', 'date' ,'duration_minutes', 'services', 'Details', 'cost', 'currency', 'time', 'provider_id')


    def __init__(self, *args, **kwargs):
        super(AdminAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['provider'].widget.attrs = {'class': 'form-control shadow', 'readonly': True}
        self.fields['provider_id'].widget = forms.HiddenInput(attrs={'class': 'hidden'})
        self.fields['booker'].widget.attrs = {'class': 'form-control shadow'}
        self.fields['date'].widget.attrs = {'class': 'form-control shadow'}
        self.fields['duration_minutes'].widget.attrs = {'class': 'form-control shadow'}
        self.fields['services'].widget.attrs = {'class': 'form-control shadow'}
        self.fields['Details'].widget.attrs = {'class': 'form-control shadow'}
        self.fields['cost'].widget.attrs = {'class': 'form-control shadow'}
        self.fields['currency'].widget.attrs = {'class': 'form-control shadow'}


class AvailabilityForm(forms.Form):
    Monday = forms.RadioSelect()
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    name = forms.CharField(max_length=128)



