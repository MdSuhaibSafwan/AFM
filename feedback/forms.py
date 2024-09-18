from django import forms
from feedback.models import Feedback


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class FeedbackFrom(forms.ModelForm):
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

    rate = forms.ChoiceField(choices=RATE, widget=forms.RadioSelect(),label= 'How is your overall experience of this platform so far?' )
    feedback_category = forms.ChoiceField(choices=FEEDBACK_CATEGORY, widget=forms.RadioSelect(),label='')
    class Meta():
        model = Feedback       
        exclude = ['user','feedback_date', 'approve','created','updated',] 
