from django.contrib import admin
from .models import FaqCategory, Faq
# Register your models here.
admin.site.register(Faq)
admin.site.register(FaqCategory)
