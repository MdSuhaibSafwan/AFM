from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from personal_information.models import MentorPersonalInformation
from AFM.tasks import send_email_notification
from datetime import timedelta
from django.utils import timezone

# @periodic_task(run_every=(crontab(minute=0, hour='*/24')), name="message_notification", ignore_result=True)
# def incomplete_profile_notification():
#     queryset = MentorPersonalInformation.objects.using(
#         'afm_personal_information').filter(
#         Q(consent4=None) | Q(consent4=False),
#         Q(admin__created_at__lt=(timezone.now() - timedelta(hours=48)))| Q(admin__created_at__gt=(timezone.now() - timedelta(hours=72))),).order_by('created_at')
#     return True