from django.contrib import admin
from .models import *
from application.models import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.
admin.site.register(Mentor)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(AfmLinkUser)
admin.site.register(MentorFeedback)
admin.site.register(MentorPublicProfileComment)
admin.site.register(Admin)
admin.site.register(School)
admin.site.register(AdditionalQuestions)
admin.site.register(FutureStudent)


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


# Data CSV import User
class UserCSVData(resources.ModelResource):
    class Meta:
        model = UserCSVImportedData
        fields = [
            "id",
            "first_name",
            "last_name",
            "user_type",
            "email",
            "date_of_birth",
            "nationality",
            "languages",
            "currently_studying_course",
            "course_studied",
            "phone",
        ]


class UserCSVDataList(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "user_type", "is_imported"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False


class UserCSVDataListAdmin(
    UserCSVDataList, ImportExportModelAdmin
):
    resource_class = UserCSVData


admin.site.register(UserCSVImportedData, UserCSVDataListAdmin)
