from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

from administration.api import DemandAndSupply
from django.contrib.auth import views as auth_views

app_name = 'messaging'

urlpatterns = [
    path('messages-list/', views.comment_list_user_twfl, name='comment_list_user_twfl'),
    path('mentor/<str:mentor_slug>/',
         views.comment_mentor_public_profile_twfl, name='comment_mentor_public_profile_twfl'),

    path('student/<str:student_slug>/',
         views.send_message_to_student, name='send_message_to_student'),
   
    path('applicant/<str:applicant_slug>/', views.comment_student_twfl, name='comment_student_twfl'),
    path('support/', views.message_admin_twfl, name='message_admin_twfl'),
    path('support/<str:school>/', views.message_admin_twfl, name='message_admin_twfl'),
    path('conversations/', views.conversations, name='conversations'),
    path('conversations-detail/<str:sender_slug>/<str:receiver_slug>/', views.conversations_detail, 
                    name='conversations_detail'),

    
    path('create-comment/<str:receiver_slug>/', views.create_comment_twfl, name='create_comment_twfl'),
    path('comment-reply/<str:comment_id>/',  views.comment_reply_twfl, name='comment_reply_twfl'),
    path('live-unread-comments/',  views.live_unread_comments, name='live_unread_comments'),
    path('user-live-unread-comments/',  views.user_live_unread_comments, name='user_live_unread_comments'),
    path('send-message/', views.send_message, name='send_message_twfl'),
    path('send-ajax-message/', views.send_ajax_message, name='send_ajax_message_twfl'),
     path('send-ajax-message-with-keyword/', views.send_ajax_message_with_keyword, name='send_ajax_message_with_keyword_twfl'),
    path('update-new-messages/', views.update_new_messages, name='update_new_messages'),
    path('check-msg-read-unread/', views.check_msg_read_unread, name='check_msg_read_unread'),
    path('clone-mentor-comment-model/', views.clone_mentor_comment_model, name='clone_mentor_comment_model'),
    path('reported-users/', views.reported_users_twfl, name='reported_users_twfl'),
    path('praised-users/', views.praised_users_twfl, name='praised_users_twfl'),
    path('block-user/<str:user_slug>/', views.block_user_twfl, name='block_user'),
    path('delete-report-user-record/<str:record_id>/', views.delete_report_record_twfl, name='delete_report_record_twfl'),
    path('praise-user/<str:user_slug>/', views.praise_user_twfl, name='praise_user'),
    path('thank-you-for-report/', TemplateView.as_view(
        template_name='messaging/thank_you_for_report.html'),
         name='thank_you_for_report'),
    path('test-unread-message-count/', views.test_unread_message_count, name='test_unread_message_count'),

]
