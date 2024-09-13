from django.contrib import admin
from .models import *
from application.models import *

# Register your models here.
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(AfmLinkUser)
admin.site.register(MentorFeedback)
admin.site.register(MentorPublicProfileComment)
admin.site.register(Admin)



class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'slug', 'username', 'email', 'is_active', ]
    ordering = ['username', ]
    search_fields = ('email',)


admin.site.register(CustomUser, UserModelAdmin)


class MentorBookingLeadsAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'date_for_appointment', 'reasone_for_an_appointment']
    ordering = ['created_at', ]


admin.site.register(MentorBookingLeads, MentorBookingLeadsAdmin)


class DemandAndSupplyAdmin(admin.ModelAdmin):
    list_display = ['spoken_language', 'country', 'subject', 'demand', 'supply']
    ordering = ['created_at', ]


admin.site.register(DemandAndSupply, DemandAndSupplyAdmin)


class InstituteAdmin(admin.ModelAdmin):
    list_display = ['institute_name', 'institute_slug']

admin.site.register(Institute, InstituteAdmin)