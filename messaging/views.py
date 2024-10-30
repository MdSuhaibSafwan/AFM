import operator
import re
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from webpush import send_user_notification
from decouple import config
from AFM.settings import MAIL_SEND_FROM
from administration.templatetags.administration_extras import getuser
from bookings.helpers import annotate_appointment
from messaging.filters import ReportUserFilter, UserFilterByName
from messaging.forms import MessagingForm, ReportUserForm, PraiseUserForm
from administration.login_check import student_parent_admin_user_required, student_parent_mentor_admin_user_required, \
    mentor_user_required, student_user_complete_profile_required, super_admin_user_required, admin_user_required, \
    mentor_has_approved_profile, student_has_application_fill_permission_required, \
    student_parent_mentor_school_admin_user_required, student_future_student_parent_school_admin_user_required, \
    student_future_student_parent_mentor_admin_user_required, \
    future_student_student_parent_mentor_school_admin_user_required, student_future_mentor_admin_user_required
from administration.models import Mentor, CustomUser, MentorPublicProfileComment, BlockUser, Parent, Student, Admin, \
    School
from messaging.models import Messaging, ReportUser, PraiseUser
from administration.forms import AdminMeetingLinkForm
from notifications.signals import notify
from personal_information.models import MentorPersonalInformation, StudentPersonalInformation, AppBasicInformation
from payments.models import *
from django.db.models import Q
from django.template import loader
from django.core.mail import send_mail
from smtplib import SMTPException

from bookings.models import UserServices, Services, Appointment
from AFM.settings import SCHOOL_ID
SCHOOL_OBJECT = None
try:
    if SCHOOL_ID:
        SCHOOL_OBJECT = School.objects.get(id=SCHOOL_ID)
except School.DoesNotExist as e:
    print(e)
    
mail_send_from = MAIL_SEND_FROM


@student_future_student_parent_school_admin_user_required
def comment_mentor_public_profile_twfl(request, mentor_slug):
    sender_slug = request.user.slug
    user_profile = CustomUser.objects.get(slug=mentor_slug)
    mentor_info = None
    mentor_personal_info = None
    if user_profile.user_type == 4:
        mentor_info = Mentor.objects.get(
            admin__slug=mentor_slug)
        mentor_personal_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
            admin__user_slug=mentor_slug)
    # Check if requested mentor is not reported by this user
    if ReportUser.objects.filter(report_by_user__in=[request.user, user_profile],
                                 reported_user__in=[request.user, user_profile],
                                 is_removed=False).exists():
        raise Http404

    report_user_form = ReportUserForm()
    praise_user_form = PraiseUserForm()

    comments = Messaging.objects.filter(sender__in=[user_profile, request.user],
                                        receiver__in=[user_profile, request.user],
                                        comment_status=True).order_by('created_at')
    comments = annotate_appointment(comments)
    unread_comments = Messaging.objects.filter(sender__in=[user_profile, request.user],
                                               receiver=request.user,
                                               read=False)
    unread_comments = annotate_appointment(unread_comments)
    unread_comments.update(read=True)

    form = MessagingForm()
    meeting_form = None
    admin_user = None
    if request.user.user_type == 0:
        admin_user = Admin.objects.first()
        meeting_form = AdminMeetingLinkForm(instance=admin_user or None)

    
    return render(request, 'messaging/new_message_mentor.html',
                  {'mentor_info': mentor_info, 'mentor_personal_info': mentor_personal_info,
                   'sender_slug':sender_slug,'user_profile': user_profile,
                   'comment_form': form, 'comments': comments, 'report_user_form': report_user_form,
                   'praise_user_form': praise_user_form, 'meeting_form': meeting_form, 'admin_user_links': admin_user})




@login_required
def send_message_to_student(request, student_slug):
    user_profile = CustomUser.objects.get(slug=student_slug)
    student = Student.objects.get(admin__slug=student_slug)
    student_personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
            admin__user_slug=student_slug)

    # Check if requested student is not reported by this user
    if ReportUser.objects.filter(report_by_user__in=[request.user, user_profile],
                                 reported_user__in=[request.user, user_profile],
                                 is_removed=False).exists():
        raise Http404

    report_user_form = ReportUserForm
    praise_user_form = PraiseUserForm

    messages = Messaging.objects.filter(sender__in=[user_profile, request.user],
                                        receiver__in=[user_profile, request.user],
                                        comment_status=True).order_by('created_at')
    
    unread_messages = Messaging.objects.filter(sender__in=[user_profile, request.user],
                                               receiver=request.user,
                                               read=False)

    form = MessagingForm()

    return render(request, 'messaging/new_message_student.html',
                  {'student': student, 'student_personal_info': student_personal_info,
                   'user_profile': user_profile,
                   'comment_form': form, 'messages': messages, 'report_user_form': report_user_form,
                   'praise_user_form': praise_user_form})







@future_student_student_parent_mentor_school_admin_user_required
def comment_list_user_twfl(request):
    admin_profile = CustomUser.objects.filter(user_type=0).first()
    list_user_sender = Messaging.objects.filter(
        Q(receiver=request.user) | Q(sender=request.user)).values_list('sender').order_by('-created_at')
    list_user_receiver = Messaging.objects.filter(
        Q(receiver=request.user) | Q(sender=request.user)).values_list('receiver').order_by('-created_at')
    list_user = list_user_sender.union(list_user_receiver)
    if request.user.user_type in [0, 1]:
        # Get all the mentors
        list_user = CustomUser.objects.filter(id__in=list_user)
        # list_user = reversed(sorted(queryset, key=lambda t: t.my_unread_messages))
    else:

        # Exclude reported users
        reported_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                   is_removed=False).values_list('reported_user')
        # Exclude users from which current user get reported from
        reported_by_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                      is_removed=False).values_list('report_by_user')
        list_user = CustomUser.objects.filter(id__in=list_user).exclude(
            id=request.user.id).exclude(Q(id__in=reported_users) | Q(id__in=reported_by_users))
        # list_user = reversed(sorted(list_user, key=lambda t: t.my_unread_messages))
    # exclude TAG support user as it is already static on top
    list_user = list_user.exclude(slug=admin_profile.slug)
    filtered_qs = UserFilterByName(request.GET, list_user)
    list_user = reversed(sorted(filtered_qs.qs, key=lambda t: t.my_unread_messages))
    # for i in list_user:
    #     print(i.first_name, i.my_unread_messages)
    # paginated_filtered = Paginator(filtered_qs.qs, 100)
    # page_number = request.GET.get('page')
    # page_obj = paginated_filtered.get_page(page_number)
    return render(request, 'messaging/applicant_comments_list.html',
                  {'list_user': list_user, 'form': filtered_qs.form, 'admin_profile': admin_profile})


@student_future_mentor_admin_user_required
@mentor_has_approved_profile
def comment_student_twfl(request, applicant_slug):
    applicant_profile = CustomUser.objects.get(slug=applicant_slug)
    mentor_late_point_link = None
    if request.user.slug == 4:
        mentor_personal_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
            admin__user_slug=request.user.slug)
        mentor_late_point_link = mentor_personal_info.late_point
    # Check if requested mentor is not reported by this user or
    # The requested mentor hasn't reported current user
    if ReportUser.objects.filter(report_by_user__in=[request.user, applicant_profile],
                                 reported_user__in=[request.user, applicant_profile],
                                 is_removed=False).exists():
        raise Http404

    report_user_form = ReportUserForm
    applicant_personal_info = None
    student_info = None
    applicant_basic_info = None
    if applicant_profile.user_type == 3:
        student_info = Student.objects.get(admin__slug = applicant_slug)
        applicant_personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
            admin__user_slug=applicant_slug)
        applicant_basic_info = AppBasicInformation.objects.using('afm_personal_information').get(
            user_slug=applicant_slug)
    comments = Messaging.objects.filter(sender__in=[applicant_profile, request.user],
                                        receiver__in=[applicant_profile, request.user],
                                        comment_status=True).order_by('created_at')
    comments = annotate_appointment(comments)

    unread_comments = Messaging.objects.filter(sender__in=[applicant_profile, request.user],
                                               receiver=request.user,
                                               read=False)
    unread_comments = annotate_appointment(unread_comments)

    unread_comments.update(read=True)
    form = MessagingForm()

    mentor_services = Services.objects.filter(is_active=True)
    paypal_acc = PaypalOnboardedSeller.objects.filter(user=request.user, permission_granted=True,
                                                      paypal_account_email_confirmed=True)

    return render(request, 'messaging/mentor_comments.html',
                  {'comment_form': form, 'comments': comments, 'applicant_profile': applicant_profile,
                   'applicant_personal_info': applicant_personal_info, 'report_user_form': report_user_form,
                   'mentor_late_point_link': mentor_late_point_link, 'student_info': student_info,
                   'applicant_basic_info': applicant_basic_info, 'services': mentor_services, 'paypal_acc': paypal_acc})


@mentor_user_required
def message_admin_twfl(request, school=None):
    if school == 'school':
        admin_profile = SCHOOL_OBJECT.admin
    else:
        admin_profile = CustomUser.objects.filter(user_type=0).first()
    comments = Messaging.objects.filter(sender__in=[admin_profile, request.user],
                                        receiver__in=[admin_profile, request.user],
                                        comment_status=True).order_by('created_at')
    unread_comments = Messaging.objects.filter(sender__in=[admin_profile, request.user],
                                               receiver=request.user,
                                               read=False)
    unread_comments.update(read=True)
    return render(request, 'messaging/admin_messaging.html',
                  {'comments': comments, 'admin_profile': admin_profile, })


@student_parent_mentor_admin_user_required
def create_comment_twfl(request, receiver_slug):
    receiver_profile = CustomUser.objects.get(slug=receiver_slug)
    if request.method == 'POST':
        form = MessagingForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.receiver = receiver_profile
            instance.sender = request.user
            instance.save()
            messages.success(request, "Your response is updated")
        else:
            messages.error(request, "Failed to save, Form is not valid")
    if request.user.user_type == 4:
        return redirect("messaging:comment_student_twfl", receiver_slug)
    return redirect("messaging:comment_mentor_public_profile_twfl", receiver_slug)


@student_parent_mentor_admin_user_required
def comment_reply_twfl(request, comment_id):
    parent = Messaging.objects.get(id=comment_id)
    if request.method != 'POST':
        messages.error(request, "Failed to reply, Form is not valid")
    else:
        Messaging.objects.create(sender=request.user,
                                 receiver=parent.receiver,
                                 comment=request.POST['comment'],
                                 parent=parent)
        messages.success(request, "Your response is updated")
    if request.user.user_type == 4:
        return redirect("messaging:comment_student_twfl", request.POST['user_profile_slug'])
    else:
        return redirect("messaging:comment_mentor_public_profile_twfl", request.POST['user_profile_slug'])


def live_unread_comments(request):
    # Exclude reported users
    if not request.user.is_authenticated:
        return JsonResponse({"unread_count": 0})
        
    reported_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                               is_removed=False).values_list('reported_user')
    # Exclude users from which current user get reported from
    reported_by_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                  is_removed=False).values_list('report_by_user')
    unread_count = Messaging.objects.filter(receiver=request.user,
                                            read=False).exclude(Q(sender=request.user) | Q(sender__in=reported_by_users)
                                                                | Q(sender__in=reported_users)).count()
    # unread_count = Messaging.objects.filter(receiver=request.user,
    #                                         read=False).exclude(sender=request.user).count()
    return JsonResponse({"unread_count": unread_count})


def user_live_unread_comments(request):
    unread_count = 0
    if not request.user.is_authenticated:
        return JsonResponse({"unread_count": unread_count})

    if request.method == 'GET':
        user_slug = request.GET['user_slug']
        if user_slug:
            unread_count = Messaging.objects.filter(sender__slug=user_slug,
                                                    receiver=request.user,
                                                    read=False).exclude(sender=request.user).count()

    return JsonResponse({"unread_count": unread_count})


@login_required()
def send_message(request):
    if request.method == 'GET':
        msg = request.GET['msg']
        receiver_slug = request.GET['receiver_slug']
        receiver_profile = CustomUser.objects.get(slug=receiver_slug)
        if ReportUser.objects.filter(report_by_user__in=[request.user, receiver_profile],
                                     reported_user__in=[request.user, receiver_profile],
                                     is_removed=False).exists():
            raise Http404
        status = None
        msg_id = None
        new_msg = None
        if msg:
            new_msg = Messaging(sender=request.user, receiver=receiver_profile, comment=msg)
            new_msg.save()
            msg_id = new_msg.id

            # Send Email Notification
            # Check if first message
            # if Messaging.objects.filter(sender=request.user, receiver=receiver_profile).count == 1:

            # Send Notification
            # payload = {
            #             "head": request.user.first_name + " sent you a message",
            #             "body": msg,
            #             "icon": "https://tag-afm-bucket.s3.amazonaws.com/static/images/default_profile.png",
            #             "url": config('AFM_LINK') + "/messages-list/",
            #             }
            # send_user_notification(user=receiver_profile, payload=payload, ttl=1000)
            status = True
        regex = re.compile('booking/confirm/[0-9]*/')
        if '/booking/confirm/' in new_msg.comment:
            if regex.findall(new_msg.comment):
                new_msg.appointment = Appointment.objects.get(
                    id=re.findall("\d+", regex.findall(new_msg.comment)[0])[0])
            else:
                new_msg.appointment = None
        else:
            new_msg.appointment = None

        if new_msg.appointment:
            return JsonResponse({
                "msg_send_status": status, "msg_id": msg_id,
                "appointment_date": new_msg.appointment.date,
                "appointment_from_time": new_msg.appointment.from_time,
                "appointment_to_time": new_msg.appointment.to_time,
                "appointment_booker_timezone": new_msg.appointment.booker.timezone,
                "appointment_provider_slug": new_msg.appointment.provider.slug,
                "appointment_services_title": new_msg.appointment.services.title,
                "appointment_duration_minutes": new_msg.appointment.duration_minutes,
                "appointment_currency": new_msg.appointment.currency,
                "appointment_id": new_msg.appointment.id,
                "user_type": getuser(request.user.user_type),
            })
    return JsonResponse({"msg_send_status": status, "msg_id": msg_id, })


@login_required()
def send_ajax_message(request):
    if request.method == 'GET':
        msg = request.GET['msg']
        receiver_slug = request.GET['receiver_slug']
        receiver_profile = CustomUser.objects.get(slug=receiver_slug)
        if ReportUser.objects.filter(report_by_user__in=[request.user, receiver_profile],
                                     reported_user__in=[request.user, receiver_profile],
                                     is_removed=False).exists():
            raise Http404
        
        new_msg = Messaging(sender=request.user, receiver=receiver_profile, comment=msg)
        new_msg.save()
        msg_id = new_msg.id
        message =  json.dumps(new_msg.comment)
        status = True
        
    return JsonResponse({"msg_send_status":status, "msg_id":msg_id, "msg":message })



@login_required()
def send_ajax_message_with_keyword(request):
    if request.method == 'GET':
        msg = request.GET['msg']
        sender_slug = request.GET['sender_slug']
        receiver_slug = request.GET['receiver_slug']
        receiver_profile = CustomUser.objects.get(slug=receiver_slug)

        # Save the original message
        if ReportUser.objects.filter(report_by_user__in=[request.user, receiver_profile],
                                     reported_user__in=[request.user, receiver_profile],
                                     is_removed=False).exists():
            raise Http404
        
        new_msg = Messaging(sender=request.user, receiver=receiver_profile, comment=msg)
        new_msg.save()
        msg_id = new_msg.id
        message =  json.dumps(new_msg.comment)
        status = True

        # Generate default mentor message for given keywords
        keyword_message = Messaging(sender=receiver_profile, receiver=request.user, 
                                    comment="Sorry, I can't advise on visas, specific fees or entry requirements, AP will advise on this after you have applied. Please ask me about the course, student life  or if you would like me to help you apply?")
        keyword_message.save()
        print("Default keyword message - ", keyword_message.comment)
        
    return JsonResponse({"msg_send_status":status, "msg_id":msg_id, "msg":message })




@login_required()
def check_msg_read_unread(request):
    status = False
    if request.method == 'GET':
        msg_id = request.GET['msg_id']
        if msg_id:
            status = Messaging.objects.filter(id=msg_id, read=True).exists()
    return JsonResponse({"msg_read_status": status})


def test_web_notification(request):
    # Send Notification
    payload = {
        "head": request.user.first_name + " sent you a message",
        "body": "Test message",
        "icon": "https://tag-afm-bucket.s3.amazonaws.com/static/images/default_profile.png",
        "url": config('AFM_LINK') + "/messages-list/",
    }
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    return redirect("administration:dashboard")


@login_required()
def update_new_messages(request):
    if request.method == 'GET':
        receiver_slug = request.GET['receiver_slug']
        receiver_profile = CustomUser.objects.get(slug=receiver_slug)
        msgs = None
        unread_msgs = Messaging.objects.filter(sender__in=[receiver_profile, request.user],
                                               receiver=request.user,
                                               read=False).order_by('created_at')
        unread_msgs = annotate_appointment(unread_msgs)
        unread_msgs = unread_msgs.first()
        print(getuser(request.user.user_type))
        if unread_msgs:
            msgs = unread_msgs.comment
            unread_msgs.read = True
            unread_msgs.save()
            if unread_msgs.appointment:
                return JsonResponse({
                    "unread_msgs": msgs,
                    "appointment_date": unread_msgs.appointment.date,
                    "appointment_from_time": unread_msgs.appointment.from_time,
                    "appointment_to_time": unread_msgs.appointment.to_time,
                    "appointment_booker_timezone": unread_msgs.appointment.booker.timezone,
                    "appointment_provider_slug": unread_msgs.appointment.provider.slug,
                    "appointment_services_title": unread_msgs.appointment.services.title,
                    "appointment_duration_minutes": unread_msgs.appointment.duration_minutes,
                    "appointment_currency": unread_msgs.appointment.currency,
                    "appointment_id": unread_msgs.appointment.id,
                    "user_type": getuser(request.user.user_type),
                })
        return JsonResponse({"unread_msgs": msgs, })


def clone_mentor_comment_model(request):
    old_model_objects = MentorPublicProfileComment.objects.all()
    for old_model_object in old_model_objects:
        new_object = Messaging(sender=old_model_object.sender,
                               receiver=old_model_object.receiver,
                               comment=old_model_object.comment,
                               comment_status=old_model_object.comment_status,
                               read=old_model_object.read,
                               created_at=old_model_object.created_at,
                               updated_at=old_model_object.updated_at)
        if not Messaging.objects.filter(sender=old_model_object.sender,
                                        receiver=old_model_object.receiver,
                                        comment=old_model_object.comment,
                                        comment_status=old_model_object.comment_status,
                                        read=old_model_object.read,
                                        created_at=old_model_object.created_at,
                                        updated_at=old_model_object.updated_at).exists():
            new_object.save()
            print(new_object)

    return redirect('/')


@student_future_student_parent_mentor_admin_user_required
def block_user_twfl(request, user_slug):
    if request.method == 'POST':
        reported_user = CustomUser.objects.get(slug=user_slug)
        print("Blocking CustomUser triggered - ", reported_user)
        report_user_form = ReportUserForm(request.POST)
        if report_user_form.is_valid():
            block_user = report_user_form.save(commit=False)
            block_user.reported_user = reported_user
            block_user.report_by_user = request.user
            block_user.save()
            # Send Notification
            verb = "You are blocked by a %s, you may not able to see this profile again in your chat " \
                   "box, Name : %s" % (getuser(request.user.user_type), request.user.first_name)
            notify.send(block_user,
                        recipient=reported_user,
                        description='#',
                        target=reported_user,
                        level='warning',
                        verb=verb)
            print(f"{block_user.reported_user} is blocked by {block_user.report_by_user} - {request.user.user_type}")
            print("Verb - ", verb)
            print("Bad Message - ", block_user.message)
        messages.success(request, "Thanks for your response ")

    return redirect('messaging:thank_you_for_report')


@student_future_student_parent_mentor_admin_user_required
def praise_user_twfl(request, user_slug):
    if request.method == 'POST':
        praised_user = CustomUser.objects.get(slug=user_slug)
        print("CustomUser that is being praised - ", praised_user)
        praise_user_form = PraiseUserForm(request.POST)
        print("Praise Form Valid - ", praise_user_form.is_valid())
        if praise_user_form.is_valid():
            praise_user = praise_user_form.save(commit=False)
            praise_user.praised_user = praised_user
            praise_user.praise_by_user = request.user
            praise_user.save()
            praise_user_form.save_m2m()

            # Send Notification
            if request.user.user_type == 3:
                verb_mentor = "You are praised by an Student, keep the good work up. " \
                              "Student Name : %s" % request.user.first_name
                notify.send(praise_user,
                            recipient=praised_user,
                            description='#',
                            target=praised_user,
                            level='success',
                            verb=verb_mentor)
                print(f"Notification of praise sent to {praised_user} by {request.user} - {request.user.user_type}")
                print("Message - ", praise_user.message)

            if request.user.user_type == 5:
                verb_mentor = "You are praised by a Parent, keep the good work up. " \
                              "Parent Name : %s" % request.user.first_name
                notify.send(praise_user,
                            recipient=praised_user,
                            description='#',
                            target=praised_user,
                            level='success',
                            verb=verb_mentor)
                print(f"Notification of praise sent to {praised_user} by {request.user} - {request.user.user_type}")
                print("Message - ", praise_user.message)
                
            if request.user.user_type == 12:
                verb_mentor = "You are praised by a student, keep the good work up. " \
                              "Student Name : %s" % request.user.first_name
                notify.send(praise_user,
                            recipient=praised_user,
                            description='#',
                            target=praised_user,
                            level='success',
                            verb=verb_mentor)
                print(f"Notification of praise sent to {praised_user} by {request.user} - {request.user.user_type}")
                print("Message - ", praise_user.message)

        messages.success(request, "Thanks for your response ")

    return redirect('messaging:comment_mentor_public_profile_twfl', user_slug)


@super_admin_user_required
def reported_users_twfl(request):
    if request.method != 'POST':
        list = ReportUser.objects.all().order_by('-updated_at')
        queryset = ReportUserFilter(request.GET, list)
        paginated_filtered = Paginator(queryset.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)
        return render(request, 'messaging/reported_users.html',
                      {'page_obj': page_obj})
    else:
        record_id = request.POST.get('record_id')
        report_user_object = get_object_or_404(ReportUser, id=record_id)
        if report_user_object.is_removed:
            report_user_object.is_removed = False
        else:
            report_user_object.is_removed = True
            # Send Notification
            verb_mentor = "Your request to report user is been deactivated now by TAG Admin. You will be able to see " \
                          "him/her again in your chat list. User Name : %s" % \
                          report_user_object.reported_user.first_name

            notify.send(report_user_object,
                        recipient=report_user_object.report_by_user,
                        description='#',
                        target=report_user_object,
                        level='warning',
                        verb=verb_mentor)

            verb_mentor = "You are reported by a user which request has been deactivated now by TAG Admin. " \
                          "You will be able to see him/her again in your chat list. " \
                          "User Name : %s" % report_user_object.report_by_user.first_name
            notify.send(report_user_object,
                        recipient=report_user_object.reported_user,
                        description='#',
                        target=report_user_object,
                        level='success',
                        verb=verb_mentor)
        report_user_object.save()
        return redirect('messaging:reported_users_twfl')


@super_admin_user_required
def delete_report_record_twfl(request, record_id):
    if request.method == 'POST':
        redirect_link = request.POST['redirect']
        report_user_object = get_object_or_404(ReportUser, id=record_id)
        report_user_object.delete()
        return redirect(redirect_link)


@super_admin_user_required
def praised_users_twfl(request):
    list = PraiseUser.objects.all()
    return render(request, 'messaging/praised_users.html',
                  {'list': list, })


def test_unread_message_count(request):
    from datetime import timedelta
    from django.utils import timezone
    unread_msgs = Messaging.objects.filter(read=False,
                                           created_at__range=(
                                           timezone.now() - timedelta(hours=1), timezone.now())).order_by('created_at')
    return HttpResponse(str(unread_msgs.count()))


@super_admin_user_required
def conversations(request):

    # conversations = Messaging.objects.filter(sender__user_type__in=[3,12]).order_by('sender','receiver','-created_at').distinct('sender','receiver')
    distinct_conversations = Messaging.objects.filter(sender__user_type__in=[3,12]).distinct('sender','receiver')
    conversations = Messaging.objects.filter(id__in=distinct_conversations).order_by('-created_at')

    print("----------------Conversations-----------------", conversations.count())
    paginated_objects= Paginator(conversations, 40)
    page_number = request.GET.get('page')
    page_obj = paginated_objects.get_page(page_number)
    context = {'conversations': conversations, 
                'page_obj': page_obj,
                }
    return render(request, "messaging/conversations.html",context)



@super_admin_user_required
def conversations_detail(request, sender_slug, receiver_slug):
    student = CustomUser.objects.get(slug=sender_slug)
    conversations = Messaging.objects.filter(
        Q(sender__slug=sender_slug, receiver__slug=receiver_slug) | 
        Q(sender__slug=receiver_slug, receiver__slug=sender_slug)
        ).order_by('created_at')
    count = conversations.count()
    print("Conversations count - ", conversations.count())
    context = {
        'student':student,
        'conversations':conversations,
        'count':count
        }

    return render(request, "messaging/conversations_detail.html", context)