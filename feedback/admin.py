from django.contrib import admin
from feedback.models import Feedback

# Register your models here.

admin.site.register(Feedback)

# class FeedbackAdmin(admin.ModelAdmin):
#     list_display = ('feedback_category', 'user', 'completed','updated')

# admin.site.register(Feedback, FeedbackAdmin)