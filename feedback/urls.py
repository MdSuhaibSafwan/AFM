from django.urls import path
from feedback import views

app_name = 'feedback'

urlpatterns = [
    path('', views.AllFeedback.as_view(), name='all_feedback'),
    path('submit-your-feedback/', views.feedback_create, name='feedback-create'),
    path('thank-you/', views.thank_you, name='thank-you'),
    path('student-feedback/', views.student_feedback, name='student-feedback'),
]
