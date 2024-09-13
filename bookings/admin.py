from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin


# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('provider', 'booker', 'status', 'date', 'from_time', 'to_time', 'cost')
    list_filter = ('status',)


class ServicesAdmin(SummernoteModelAdmin):
    list_display = ('title', 'is_active', 'approved')
    list_filter = ('is_active', 'approved')
    summernote_fields = ('description',)


class ReasonsAdmin(admin.ModelAdmin):
    search_fields = ('Reason',)


class TimeSlotsAdmin(admin.ModelAdmin):
    list_display = ('from_time', 'to_time', 'date', 'provider', 'available')
    list_filter = ('available', 'provider__email')
    search_fields = ('provider__email',)


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Reasons, ReasonsAdmin)
admin.site.register(Services, ServicesAdmin)
admin.site.register(UserServices)
admin.site.register(Timeslots, TimeSlotsAdmin)
