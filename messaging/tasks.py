from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from messaging.models import Messaging
from personal_information.models import CustomUserPersonalInformation
from decouple import config
from AFM.tasks import send_email_notification
from datetime import timedelta
from django.utils import timezone

logger = get_task_logger(__name__)

def create_message_notification_email(unread_msgs):
    
    for message in unread_msgs:
        print("Message Object - ", message.id, message.sender.slug)
        link = ''.join([config('AFM_LINK'), '/message/messages-list/'])
        sender_full_name = F"{message.sender.first_name} {message.sender.last_name}"
        receiver_full_name = F"{message.receiver.first_name} {message.receiver.last_name}"
        print("Slug - ", message.sender.slug)
        
        comment = message.comment
        msg = F"You have new message from {sender_full_name}"
        if message.sender.user_type == 12:
            pic = ''.join([config('AFM_LINK'), '/static/images/default_profile.png'])
        if message.sender.user_type in [0,1,3,4]:
            custom_sender = CustomUserPersonalInformation.objects.get(user_slug = message.sender.slug)
            if custom_sender.profile_pic:
                pic = F"{custom_sender.profile_pic.url}"
            else:
                pic = ''.join([config('AFM_LINK'), '/static/images/default_profile.png'])

        
        print("Pic = ", pic)
        print(F"""
                Message object cluster - 
                sender - {message.sender},
                sender slug - {message.sender.slug},
                receiver - {message.receiver},
                picture - {pic},
                comment - {comment}
                """)

        # Celery task
        send_email_notification.delay('You have a new message',
                                        'email/unread_message_notification_email.html',
                                        [message.receiver.email,],
                                        {
                                            'sender': sender_full_name,
                                            'receiver': receiver_full_name,
                                            'comment':comment,
                                            'msg': msg,
                                            'link': link,
                                            'pic':pic
                                        }
                                        )
        print("Email notification logger.....")
        logger.info("Email Notification has sent")


# Celery beat periodic task (every 1 hour) 
@periodic_task(run_every=(crontab(minute=0, hour='*/1')), name="unread_message_notification_email", ignore_result=True)
def unread_message_notification_email():
    unread_msgs = Messaging.objects.filter(read=False,
                                           created_at__range=(timezone.now() - timedelta(hours=1), timezone.now())
                                           ).order_by('created_at')
    print("Unread Messages - ", unread_msgs)
    if unread_msgs:
        create_message_notification_email(unread_msgs)
   




#-----------------------------------------Old Notification Periodic Task----------------------------------------#

# def create_message_notification(unread_msgs):
#     unread_msgs_list = []
#     temp = []
#     for unread_msg in unread_msgs:
#         if unread_msg.receiver:
#             if unread_msg.receiver.email not in temp:
#                 if unread_msg.receiver.user_type == 4 and unread_msg.receiver.mentor.profile_status == False:
#                     pass
#                 else:
#                     temp.append(unread_msg.receiver.email)
#                     unread_msgs_list.append(unread_msg)
#     # print(receivers, 'List of users for email notification')
#     if unread_msgs_list:
#         for unread_msg in unread_msgs_list:
#             link = ''.join(
#                 [config('AFM_LINK'), '/message/messages-list/'])
#             first_name = unread_msg.receiver.first_name
#             msg = 'Just to let you know you have new unread messages in your profile. ' \
#                   'Please log in to view the message and continue ' \
#                   'the conversation.'
#             if unread_msg.receiver.user_type == 3:
#                 if unread_msg.receiver.personal_info_subject() and int(
#                         unread_msg.receiver.personal_info_subject()) != 6:
#                     link = ''.join(
#                         [config('AFM_LINK'), '/message/messages-list/'])

#             if unread_msg.receiver.user_type == 4:
#                 # msg = 'This is just to let you know that you have new messages waiting to be read.' \
#                 #       ' These could be from a potential Mentee, a Parent on the TAG Team, so please' \
#                 #       ' log in and reply when you can and keep the conversation flowing!'
                
#                 msg = 'You have just received a new message. Please log in ASAP to chat live or leave a reply.'
                
                
#                 if unread_msg.receiver.mentor_subject() and int(unread_msg.receiver.mentor_subject()) != 6:
#                     link = ''.join(
#                         [config('AFM_LINK'), '/message/messages-list/'])

#             if unread_msg.receiver.user_type == 5:
#                 if unread_msg.sender.user_type == 3:
#                     if unread_msg.sender.personal_info_subject() and int(
#                             unread_msg.sender.personal_info_subject()) != 6:
#                         link = ''.join(
#                             [config('AFM_LINK'), '/message/messages-list/'])
#                 if unread_msg.sender.user_type == 4:
#                     if unread_msg.sender.mentor_subject() and int(unread_msg.sender.mentor_subject()) != 6:
#                         link = ''.join(
#                             [config('AFM_LINK'), '/message/messages-list/'])

#             send_email_notification.delay('You have a new message',
#                                           'email/notification_mail.html',
#                                           [unread_msg.receiver.email],
#                                           {
#                                               'first_name': first_name,
#                                               'msg': msg,
#                                               'link': link
#                                           }
#                                           )
#             print("Email notification logger.....")
#             logger.info("Email Notification has sent")

#     else:
#         logger.info("No users to notify!")



# # Periodic task that runs for the first minute on every hour
# @periodic_task(run_every=(crontab(minute=0, hour='*/1')), name="unread_message_notification_email", ignore_result=True)
# def unread_message_email():
#     unread_msgs = Messaging.objects.filter(read=False,
#                                            created_at__range=(timezone.now() - timedelta(hours=1), timezone.now())
#                                            ).order_by('created_at')
#     create_message_notification(unread_msgs)


#-----------------------------------------Old Notification Periodic Task----------------------------------------#