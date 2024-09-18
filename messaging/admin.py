from django.contrib import admin
# Register your models here.
from messaging.models import Messaging, ReportUser, PraiseUserChoice, PraiseUser

admin.site.register(ReportUser)
admin.site.register(PraiseUserChoice)
admin.site.register(PraiseUser)


class ModelMessaging(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'comment', 'read', 'created_at' ]
    ordering = ['id', ]

admin.site.register(Messaging, ModelMessaging )
