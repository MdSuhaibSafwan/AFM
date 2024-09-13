from django.contrib import admin
from .models import *
from application.models import *

admin.site.register(ApplicationAppliedAtUniversityLogin)
admin.site.register(ApplicationOfferStatus)
admin.site.register(EnglishLanguage)
admin.site.register(ApplicationFeedback)
admin.site.register(AcademicQualification)

class ModelConsideredApplication(admin.ModelAdmin):
    list_display = ['id', 'institute', 'course_name', 'email', ]
    ordering = ['id', ]
    search_fields = ('email',)

class ModelApplication(admin.ModelAdmin):
    list_display = ['id', 'slug']
    ordering = ['id', ]
    search_fields = ('slug',)

class ModelApplicationLog(admin.ModelAdmin):
    list_display = ['id', 'app', 'admin', 'considered_app',]
    ordering = ['id', ]
    search_fields = ('id',)

class ModelApplicationComment(admin.ModelAdmin):
    list_display = ['id', 'app', 'app_admin',]
    ordering = ['id', ]
    search_fields = ('id',)

class ModelDocumentUpload(admin.ModelAdmin):
    list_display = ['id', 'app', 'admin', 'doc_type', 'upload']
    ordering = ['id', ]
    search_fields = ('id',)

admin.site.register(Application, ModelApplication)
admin.site.register(ConsideredApplication, ModelConsideredApplication)
admin.site.register(ApplicationLog, ModelApplicationLog)
admin.site.register(ApplicationComment, ModelApplicationComment)
admin.site.register(DocumentUpload, ModelDocumentUpload)