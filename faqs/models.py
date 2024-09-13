from django.db import models
from django.urls import reverse
from administration.models import CustomUser
from ckeditor.fields import RichTextField

# Create your models here.
class FaqCategory(models.Model):
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_update_url(self):
        return reverse('faqs:fcategory-update', kwargs={'pk': self.pk})


class Faq(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True )
    user_type_data = (
        (0, 'All Users'),
        (2, 'Institute'),
        (3, 'Student'),
        (4, 'Mentor'),
        (5, 'Parent'),
        (6, 'Institute admin'),
        (7, 'App admin'),
        (8, 'Recruiter'),
        (9, 'System Mentor'),
        (10, 'System Recruiter'),
    )
    user_type = models.PositiveIntegerField(choices=user_type_data, null=True)
    category = models.ForeignKey(FaqCategory, on_delete=models.CASCADE,  null=True, blank=True)
    title = models.CharField(max_length=100)
    description = RichTextField()
    rank =  models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)
    STATUS = (
        ('publish', 'Publish'),
        ('draft','Draft'),
    )
    status = models.CharField(choices=STATUS, max_length=50)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("faqs:faq-detail", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse('faqs:faq-update', kwargs={'pk': self.pk})