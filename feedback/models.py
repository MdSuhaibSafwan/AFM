from django.db import models
from administration.models import CustomUser
from django.urls import reverse
# Create your models here.

# RATE tuple for providing rating 1 to 5 in model as choices
RATE=(
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5,5)
    )
FEEDBACK_CATEGORY = (
    ('Bug','Bug'),
    ('Suggest', 'Suggest'),
    ('Content','Content'),
    ('Praise/like','Praise/like'),
    ('Other','Other'),
    )

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATE)
    feedback_category = models.CharField(max_length=20,choices=FEEDBACK_CATEGORY)
    description = models.TextField()
    feedback_date = models.DateField(auto_now=True)
    approve = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.feedback_category

    def get_absolute_url(self):
        return reverse('feedback:feedback-detail', kwargs={'pk': self.pk})
