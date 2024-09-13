from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from bookings.models import Appointment, Services
from notifications.signals import notify
from datetime import datetime, timedelta


@receiver(post_save, sender=Appointment)
def function(sender, instance, created, **kwargs):
    verb = 'Appointment booked'
    if not created and instance.status == 'Approved':
        subject = "Booking At ApplyPeer"
        message = "Hi, " + instance.booker.first_name + "\n Your appointment with, " + instance.provider.first_name + " " \
                  + instance.provider.last_name + " on " + str(instance.date) + " at " + str(
            instance.from_time) + ".\n is " + instance.status + " by porvider."
        to_email = str(instance.booker)
        send_mail(
            subject,
            message,
            'applypeerdev@gmail.com',
            [to_email],
            fail_silently=False,
        )
        notify.send(instance,
                    recipient=instance.provider,
                    description='#',
                    target=instance,
                    level='info',
                    verb=verb,
                    # emailed=True,
                    )

        notify.send(instance,
                    recipient=instance.provider,
                    description='#',
                    target=instance,
                    level='info',
                    verb=verb,
                    # emailed=True,
                    )

    elif created:
        subject = "Booking At ApplyPeer"
        message = "Hi, " + instance.booker.first_name + "\n Your appointment with, " + instance.provider.first_name + " " \
                  + instance.provider.last_name + " on " + str(instance.date) + " at " + str(
            instance.from_time) + ".\n is " + instance.status + " by porvider."
        to_email = str(instance.booker)
        send_mail(
            subject,
            message,
            'applypeerdev@gmail.com',
            [to_email],
            fail_silently=False,
        )

        notify.send(instance,
                    recipient=instance.provider,
                    description='#',
                    target=instance,
                    level='info',
                    verb=verb,
                    # emailed=True,
                    )

        notify.send(instance,
                    recipient=instance.booker,
                    description='#',
                    target=instance,
                    level='info',
                    verb=verb,
                    # emailed=True,
                    )


@receiver(pre_save, sender=Services)
def function_approve_notification(sender, instance, **kwargs):
    if instance.id is None:
        pass

    else:
        current = instance
        previous = Services.objects.get(id=instance.id)

        if previous.approved:
            pass
        elif previous.approved == True and current.approved == True:
            subject = "Service Approved by ApplyPeer"
            message = "Hi, " + instance.provider.first_name + "\n Your service, " + instance.title + " " \
                      + "has been approved by ApplyPeer."
            to_email = str(instance.booker)
            send_mail(
                subject,
                message,
                'applypeerdev@gmail.com',
                [to_email],
                fail_silently=False,
            )
        else:
            pass
