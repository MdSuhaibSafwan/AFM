# from celery.decorators import task
from django.core.mail import send_mail
from django.template import loader
from smtplib import SMTPException
#
#
# @task(name="celery_send_email_notification")
def send_email_notification(subject, template_path_string, recipient_list, var_dict):
    html_message = loader.render_to_string(template_path_string, var_dict)
    try:
        # Send email
        send_mail(subject, "", None, recipient_list,
                         html_message=html_message)
    except SMTPException as e:
        return False
    else:
        return True
#
#
# @task(name="celery_test")
# def test():
#     print('Celery worked successfully')
#     return True
