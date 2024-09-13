from django.db import models
from administration.models import CustomUser
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from .choices import STATUS_CHOICES


# Create your models here.

class Services(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=250)
    duration = models.DurationField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    approved = models.BooleanField(default=False)
    denial_message = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Services, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Services'
        verbose_name_plural = 'Services'


class Reasons(models.Model):
    Reason = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Reasons'
        verbose_name_plural = 'Reasons'

    def __str__(self):
        return f'{self.Reason}'


class Appointment(models.Model):
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="service_provider")
    booker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="service_booker")

    date = models.DateField(auto_now=False)

    from_time = models.TimeField(auto_now=False)
    to_time = models.TimeField(auto_now=False)
    duration_minutes = models.PositiveIntegerField(default=10)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    meeting_link = models.URLField(max_length=3000, null=True, blank=True)
    services = models.ForeignKey(Services, on_delete=models.CASCADE)

    Reasons = models.ManyToManyField(Reasons, blank=True)
    Details = models.TextField(default='I am scheduling an appointment for...')

    InitiateRefund = models.BooleanField(default=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    cost = models.PositiveIntegerField(default=20)
    currency = models.CharField(max_length=5, default='USD')

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointment'


class UserServices(models.Model):
    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(Services, on_delete=models.CASCADE, related_name='service')
    price = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.provider} / {self.service} / {self.price}'


class Timeslots(models.Model):
    available = models.BooleanField(default=True)

    from_time = models.TimeField(auto_now=False)
    to_time = models.TimeField(auto_now=False)

    date = models.DateField(auto_now=False, auto_now_add=False)

    provider = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='Timeslots')

    def __str__(self):
        return f'{self.available}'

    class Meta:
        verbose_name = 'Timeslots'
        verbose_name_plural = 'Timeslots'


class AppointmentCancelRequests(models.Model):
     Appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
     Mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

     approved = models.BooleanField(default=False)

     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     class Meta:
         verbose_name = 'Appointment Cancellation request'
         verbose_name_plural = 'Appointment Cancellation requests'