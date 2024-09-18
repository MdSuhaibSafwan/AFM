from django.contrib import admin
from personal_information.models import *

# Register your models here.
admin.site.register(FoundationProvider)
admin.site.register(SpokenLanguage)
admin.site.register(Hobby)
admin.site.register(SubjectFoundation)
admin.site.register(TutoringSubject)
admin.site.register(TutoringWith)
admin.site.register(TutoringInLevel)
admin.site.register(PreferredLocation)
admin.site.register(SkillsToDevelop)


class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = ['user_slug','country','created_at']
    ordering = ['created_at',]

admin.site.register(CustomUserPersonalInformation,CustomUserModelAdmin)
  
class MentorModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'admin','studying_in','currently_studying','study_year','subject','programme_level', 'created_at']
    ordering = ['currently_studying',]
    
admin.site.register(MentorPersonalInformation,MentorModelAdmin)

class StudentModelAdmin(admin.ModelAdmin):
    list_display = ['admin','id','currently_studying','area_of_study','programme_level',]
    ordering = ['currently_studying',]
    
admin.site.register(StudentPersonalInformation,StudentModelAdmin)


class PreferredCareerFieldModelAdmin(admin.ModelAdmin):
    list_display = ['preferred_career_field', 'order_rank', 'status']
    ordering = ['-order_rank',]

admin.site.register(PreferredCareerField,PreferredCareerFieldModelAdmin)