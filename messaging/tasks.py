from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from messaging.models import Messaging
from decouple import config
from AFM.tasks import send_email_notification
from datetime import timedelta
from django.utils import timezone

logger = get_task_logger(__name__)
def create_message_notification(unread_msgs):
    unread_msgs_list = []
    temp = []
    for unread_msg in unread_msgs:
        if unread_msg.receiver:
            if unread_msg.receiver.email not in temp:
                if unread_msg.receiver.user_type == 4 and unread_msg.receiver.mentor.profile_status == False:
                    pass
                else:
                    temp.append(unread_msg.receiver.email)
                    unread_msgs_list.append(unread_msg)
    # print(receivers, 'List of users for email notification')
    if unread_msgs_list:
        for unread_msg in unread_msgs_list:
            link = ''.join(
                [config('AFM_LINK'), '/message/messages-list/'])
            first_name = unread_msg.receiver.first_name
            msg = 'Just to let you know you have new unread messages in your profile. ' \
                  'Please log in to view the message and continue ' \
                  'the conversation.'
            if unread_msg.receiver.user_type == 3:
                if unread_msg.receiver.personal_info_subject() and int(
                        unread_msg.receiver.personal_info_subject()) != 6:
                    link = ''.join(
                        [config('AFU_LINK'), '/message/messages-list/'])

            if unread_msg.receiver.user_type == 4:
                msg = 'This is just to let you know that you have new messages waiting to be read.' \
                      ' These could be from a potential Mentee, a Parent on the TAG Team, so please' \
                      ' log in and reply when you can and keep the conversation flowing!'
                if unread_msg.receiver.mentor_subject() and int(unread_msg.receiver.mentor_subject()) != 6:
                    link = ''.join(
                        [config('AFU_LINK'), '/message/messages-list/'])

            if unread_msg.receiver.user_type == 5:
                if unread_msg.sender.user_type == 3:
                    if unread_msg.sender.personal_info_subject() and int(
                            unread_msg.sender.personal_info_subject()) != 6:
                        link = ''.join(
                            [config('AFU_LINK'), '/message/messages-list/'])
                if unread_msg.sender.user_type == 4:
                    if unread_msg.sender.mentor_subject() and int(unread_msg.sender.mentor_subject()) != 6:
                        link = ''.join(
                            [config('AFU_LINK'), '/message/messages-list/'])

            send_email_notification.delay('You have a new message',
                                          'messaging/notification_mail.html',
                                          [unread_msg.receiver.email],
                                          {
                                              'first_name': first_name,
                                              'msg': msg,
                                              'link': link
                                          }
                                          )
            logger.info("Email Notification has sent")

    else:
        logger.info("No users to notify!")

# @periodic_task(run_every=(crontab(minute=0, hour='*/24')), name="message_notification", ignore_result=True)
# def message_notification():
#     unread_msgs = Messaging.objects.filter(read=False).order_by('created_at')
#     create_message_notification(unread_msgs)


@periodic_task(run_every=(crontab(minute=0, hour='*/1')), name="message_notification", ignore_result=True)
def message_instant_notification():
    unread_msgs = Messaging.objects.filter(read=False,
                                           created_at__range=(timezone.now() - timedelta(hours=1), timezone.now())).order_by('created_at')
    create_message_notification(unread_msgs)

