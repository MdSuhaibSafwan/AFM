from django.core.mail import send_mail
from django.template import loader
from smtplib import SMTPException
from django.conf import settings



def send_email_notification(subject, template_path_string, recipient_list, var_dict):
    html_message = loader.render_to_string(template_path_string, var_dict)
    try:
        # Send email
        send_mail(subject, "", settings.MAIL_SEND_FROM, recipient_list,
                         html_message=html_message)
        print("--------------------------Celery Email-----------------------------")
        print("Email Recipient - ", recipient_list)
        print("Email Subject - ", subject)
        print("Email - ", html_message)
        print("--------------------------Celery Email sent successfully-----------------------------")

    except SMTPException as e:
        print("SMTP Celery Email error - ", e)
        return False
    else:
        return True


def test():
    print('Celery worked successfully')
    return True
