from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from AFM.settings import MAIL_SEND_FROM
from administration.models import CustomUser, Lead, Institute, Student, Mentor, AppAdmin, Recruiter, Parent
from administration.templatetags.administration_extras import getsubject
from personal_information.models import CustomUserPersonalInformation, StudentPersonalInformation, \
    MentorPersonalInformation, AppBasicInformation, AppAddress, \
    AppPassportInformation
from application.models import Application, EnglishLanguage, VisaHistory, PersonalStatement, Reference, \
    ProfessionalExperience, ProfessionalTrainingCertificate, AcademicQualification, ApplicationLog, \
    ApplicationAppliedAtUniversityLogin, ApplicationOfferStatus, ConsideredApplication, OmittedApp, \
    DirectApplication, ApplicationFeedback, \
    DocumentUpload, ApplicationComment
from AFM.utils import unique_slug_generator
from notifications.signals import notify
from AFM.utils import get_current_request
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template import loader
from decouple import config
from django.contrib.sites.shortcuts import get_current_site
from AFM.tasks import send_email_notification

from bookings.models import Services,UserServices

'''
Function   : send_email_notification_for_application 
Description: Display all the mentors available, student can select his/her mentors
Parameters : Application object, Message string
Return     : Sent email function
'''


def send_email_notification_for_application(app, msg):
    request = get_current_request()
    mail_send_from = MAIL_SEND_FROM
    link = ''.join(['https://', get_current_site(request).domain, '/application/application/', str(app.slug)])
    # print(link, 'Application page Link')
    send_email_notification('Notification from TAG',
                                  'application/notification_mail.html',
                                  [mail_send_from],
                                  {
                                      'link': link,
                                      'msg': msg,
                                  }
                                  )

'''
Function   : pre_save_title_slug 
Description: Create unique slug every time new field is created 
Parameters : Model instance
Return     : Sent email function
'''


def pre_save_title_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_title_slug, sender=CustomUser)
pre_save.connect(pre_save_title_slug, sender=Lead)
pre_save.connect(pre_save_title_slug, sender=Application)


'''
Function   : On_Create_Super_User_Update 
Description: Create Super User
Parameters : CustomUser Instance
Return     : Create user type super user
'''


@receiver(pre_save, sender=CustomUser)
def On_Create_Super_User_Update(sender, instance: Application, **kwargs):
    if instance.is_superuser:
        instance.user_type = 0


'''
Function   : create_user_profile 
Description: Create user objects of respective models and notification for superuser
Parameters : CustomUser Instance
Return     : Create blank object of CustomUser in respective user object
'''


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        super_admin = CustomUser.objects.filter(user_type=0)
        # If user is a Institute
        if instance.user_type == 2:
            Institute.objects.create(admin=instance)
        # If user is a Student
        if instance.user_type == 3:
            # Create blank objects
            Student.objects.create(admin=instance)
            user = CustomUserPersonalInformation.objects.using('afm_personal_information').create(
                user_slug=instance.slug,
                first_name=instance.first_name,
                last_name=instance.last_name)
            StudentPersonalInformation.objects.using('afm_personal_information').create(admin=user, area_of_study=6)
            app = Application.objects.create(admin=instance, subject=6)
            EnglishLanguage.objects.create(app=app)
            VisaHistory.objects.create(app=app)
            ApplicationFeedback.objects.create(app=app)
            Reference.objects.create(app=app)
            ProfessionalExperience.objects.create(app=app)
            ProfessionalTrainingCertificate.objects.create(app=app)
            AcademicQualification.objects.create(app=app)
            PersonalStatement.objects.create(app=app)

            # Create blank object In personal information database
            app_pi = AppBasicInformation.objects.using('afm_personal_information').create(app=app.id,
                                                                                          user_slug=instance.slug,
                                                                                          first_name=instance.first_name,
                                                                                          surname=instance.last_name,
                                                                                          email=instance.email)
            AppAddress.objects.using('afm_personal_information').create(app=app_pi)
            AppPassportInformation.objects.using('afm_personal_information').create(app=app_pi)
            url_name = '#'
            verb = 'New student registered as %s' % instance.first_name
            for person in super_admin:
                # Send notification to super-admin(S)
                notify.send(instance,
                            recipient=person,
                            description=url_name,
                            target=instance,
                            level='info',
                            verb=verb)
        # If user is a Mentor
        if instance.user_type == 4:
            Mentor.objects.create(admin=instance)
            user = CustomUserPersonalInformation.objects.using('afm_personal_information').create(
                user_slug=instance.slug,
                first_name=instance.first_name,
                last_name=instance.last_name)
            MentorPersonalInformation.objects.using('afm_personal_information').create(admin=user, currently_studying=6)
            service = Services.objects.order_by('-id').first()
            UserServices.objects.create(provider=instance, service=service)

            url_name = '#'
            verb = 'New Mentor registered as %s' % instance
            # Send super-admin notification
            for person in super_admin:
                notify.send(instance,
                            recipient=person,
                            description=url_name,
                            target=instance,
                            level='info',
                            verb=verb)
        # If user is a AppAdmin
        if instance.user_type == 7:
            AppAdmin.objects.create(admin=instance)
        # If user is a Recruiter
        if instance.user_type == 8:
            Recruiter.objects.create(admin=instance)
        # If user is a Parent
        if instance.user_type == 5:
            Parent.objects.create(admin=instance)
            url_name = '#'
            verb = 'New Parent registered as %s' % instance
            for person in super_admin:
                notify.send(instance,
                            recipient=person,
                            description=url_name,
                            target=instance,
                            level='info',
                            verb=verb)
        verb = 'Welcome to AFM %s' % instance.first_name
        # Send user notification
        notify.send(instance,
                    recipient=instance,
                    description='#',
                    target=instance,
                    level='info',
                    verb=verb)


'''
Function   : auto_username_create 
Description: Set username as email of user
Parameters : CustomUser Instance
Return     : Create blank object of CustomUser in respective user object
'''


def auto_username_create(sender, instance, *args, **kwargs):
    if not instance.username:
        instance.username = instance.email.lower()


pre_save.connect(auto_username_create, sender=CustomUser)

'''
Function   : on_application_status_change 
Description: Send user notification when form status changes,
            Delete old visa history objects and create new one when study destination(S) get updated
Parameters : Application Instance
Return     : Create Notification and Visa history object(S)
'''


@receiver(pre_save, sender=Application)
def on_application_status_change(sender, instance: Application, **kwargs):
    # Get Request attribute
    request = get_current_request()
    current_user = request.user

    if instance.id is not None:
        previous = Application.objects.get(id=instance.id)
        if previous.status != instance.status:  # field will be updated
            if instance.status == 0:
                status = 'Approved'
                type = 0
            elif instance.status == 1:
                status = 'Rejected'
                type = 1
            elif instance.status == 2:
                if previous.status == 1:
                    status = 'Resubmitted'
                else:
                    status = 'Submitted'
                type = 2
            elif instance.status == 3:
                status = 'Incomplete'
                type = 3
            else:
                status = 'Interrupted By System'

            MESSAGE = "Application id {} is {}".format(instance.slug, status)
            # Save Application log
            ApplicationLog.objects.create(type=type, app=instance, message=MESSAGE, admin=current_user)
            url_name = '/application/application/%s' % (instance.slug)
            app_admin = CustomUser.objects.filter(user_type=7)
            sender = CustomUser.objects.get(id=instance.admin.id)
            # Send App-admin notification when Application is Approved or Submitted
            # (0, 'Approved'),
            # (1, 'Rejected'),
            # (2, 'Completed'),
            # (3, 'Incomplete'),
            if instance.status in [0, 2]:
                for person in app_admin:
                    notify.send(sender,
                                recipient=person,
                                description=url_name,
                                target=instance,
                                level='info',
                                verb=MESSAGE)

        if previous.study_destination_country != instance.study_destination_country:
            visa_history_instances = VisaHistory.objects.filter(app=previous)
            # Create or delete VisaHistory object based on study destination country(S) field
            for visa_history_instance in visa_history_instances:
                visa_history_instance.delete()
            for study_destination_country in instance.study_destination_country:
                VisaHistory.objects.create(app=instance, study_destination_country=study_destination_country.code)


'''
Function   : on_application_applied_at_institute 
Description: Create log for direct application 
Parameters : ApplicationAppliedAtUniversityLogin Instance
Return     : Create Application Log
'''


@receiver(post_save, sender=ApplicationAppliedAtUniversityLogin)
def on_application_applied_at_institute(sender, instance, created, **kwargs):
    # Get Request attribute
    request = get_current_request()
    current_user = request.user
    if created:
        MESSAGE = 'Application submitted on %s to %s.' % (instance.date, instance.institute.institute_name)
        ApplicationLog.objects.create(app=instance.app, message=MESSAGE, admin=current_user)


'''
Function   : on_application_omitted 
Description: Create log for omitted application 
Parameters : OmittedApp Instance
Return     : Create Application Log
'''


@receiver(post_save, sender=OmittedApp)
def on_application_omitted(sender, instance, created, **kwargs):
    # Get Request attribute
    request = get_current_request()
    current_user = request.user

    if created:
        MESSAGE = 'Application omitted by %s institute.' % (instance.institute.institute_name)
        ApplicationLog.objects.create(type=4, app=instance.app, message=MESSAGE, admin=current_user)


'''
Function   : on_application_reconsidered 
Description: Create log for reconsidered application 
Parameters : OmittedApp Instance
Return     : Create Application Log
'''


@receiver(pre_delete, sender=OmittedApp)
def on_application_reconsidered(sender, instance, using, **kwargs):
    # Get Request attribute
    request = get_current_request()
    current_user = request.user

    MESSAGE = 'Application reconsidered by %s institute.' % (instance.institute.institute_name)
    ApplicationLog.objects.create(type=5, app=instance.app, message=MESSAGE, admin=current_user)


'''
Function   : on_considered_application 
Description: Check if application is considered by institute and 
             Send notifications, Create Application log, sent email
Parameters : ConsideredApplication Instance
Return     : Send notifications, Create Application log, sent email
'''


@receiver(pre_save, sender=ConsideredApplication)
def on_considered_application(sender, instance: ConsideredApplication, **kwargs):
    # Get Request attribute
    request = get_current_request()
    current_user = request.user

    if instance.id is not None:
        previous = ConsideredApplication.objects.get(id=instance.id)
        app_admin = CustomUser.objects.filter(user_type=7)
        if instance.app_status_by_institute is not None:
            if previous.app_status_by_institute != instance.app_status_by_institute:  # field will be updated
                if instance.app_status_by_institute == 1:
                    offer = 'make a formal application'
                elif instance.app_status_by_institute == 2:
                    offer = 'request documents'
                elif instance.app_status_by_institute == 3:
                    offer = 'interview'
                else:
                    offer = 'Interrupted By System'

                MESSAGE = 'Application has offer from %s institute : %s.' % (instance.institute.institute_name, offer)
                # Create Log
                ApplicationLog.objects.create(type=6, app=instance.app, message=MESSAGE, admin=current_user,
                                              considered_app=instance)

        if instance.email is not None:
            if previous.email != instance.email:  # field will be updated
                MESSAGE = 'Application has been applied to %s institute by app-admin %s.' % (
                    instance.institute.institute_name, instance.admin.firstname + instance.admin.lastname)
                # Create Log
                ApplicationLog.objects.create(type=7, app=instance.app, message=MESSAGE, admin=current_user,
                                              considered_app=instance)

        if instance.offer_status is not None:
            if previous.offer_status != instance.offer_status:  # field will be updated
                if instance.offer_status == 0:
                    offer_status = 'In Process'
                elif instance.offer_status == 1:
                    offer_status = 'Conditional'
                elif instance.offer_status == 2:
                    offer_status = 'Unconditional'
                elif instance.offer_status == 3:
                    offer_status = 'Unsuccessful'
                else:
                    offer_status = 'Interrupted By System'

                MESSAGE = 'Application offer status for %s institute is updated to %s.' % (
                    instance.institute.institute_name, offer_status)
                print(MESSAGE)
                ApplicationLog.objects.create(type=8, app=instance.app, message=MESSAGE, admin=current_user,
                                              considered_app=instance)

        if instance.offer_select is not None:
            if previous.offer_select != instance.offer_select:  # field will be updated
                MESSAGE = 'Student has accepted offer from %s institute.' % (instance.institute.institute_name)
                # Create Log
                ApplicationLog.objects.create(type=9, app=instance.app, message=MESSAGE, admin=current_user,
                                              considered_app=instance)
                url_name = '/application/application/%s' % (instance.app.slug)
                for person in app_admin:
                    # Send notification
                    notify.send(current_user,
                                recipient=person,
                                description=url_name,
                                target=instance.app,
                                level='info',
                                verb=MESSAGE)
                # Sent email notification
                send_email_notification_for_application(instance.app, MESSAGE)

        if instance.final_selection is not None:
            if previous.final_selection != instance.final_selection:  # field will be updated
                MESSAGE = 'Student has selected offer from %s institute as his/her final selection.' % (
                    instance.institute.institute_name)
                # Create Log
                ApplicationLog.objects.create(type=10, app=instance.app, message=MESSAGE, admin=current_user,
                                              considered_app=instance)
                url_name = '/application/application/%s' % (instance.app.slug)
                for person in app_admin:
                    # Send notification
                    notify.send(current_user,
                                recipient=person,
                                description=url_name,
                                target=instance.app,
                                level='info',
                                verb=MESSAGE)
                # Sent email notification
                send_email_notification_for_application(instance.app, MESSAGE)


'''
Function   : On_Personal_Info_Update 
Description: Update user personal information in personal_information database
Parameters : CustomUserPersonalInformation Instance
Return     : Update CustomUser object
'''


@receiver(post_save, sender=CustomUserPersonalInformation)
def On_Personal_Info_Update(sender, instance, created, **kwargs):
    user = CustomUser.objects.get(slug=instance.user_slug)
    user.first_name = instance.first_name
    user.last_name = instance.last_name
    user.save()


'''
Function   : On_Create_Direct_Application 
Description: Create PersonalStatement for ConsideredApplication
Parameters : CustomUserPersonalInformation Instance
Return     : Create PersonalStatement object
'''


@receiver(post_save, sender=ConsideredApplication)
def On_Create_Direct_Application(sender, instance, created, **kwargs):
    if created:
        if instance.is_direct_app:
            PersonalStatement.objects.create(considered_application=instance)


'''
Function   : On_Create_Direct_Application 
Description: Create PersonalStatement for every ConsideredApplication
Parameters : ConsideredApplication Instance
Return     : Create PersonalStatement object
'''


@receiver(pre_save, sender=ConsideredApplication)
def On_Change_Direct_Application(sender, instance: ConsideredApplication, **kwargs):
    if instance.id is not None:
        previous = ConsideredApplication.objects.get(id=instance.id)
        if instance.institute is not None:
            if previous.institute != instance.institute:  # field will be updated
                if PersonalStatement.objects.filter(institute=previous.institute, app=previous.app).exists():
                    ps_object = PersonalStatement.objects.filter(institute=previous.institute,
                                                                 app=previous.app).first()
                    ps_object.institute = instance.institute
                    ps_object.save()
        else:
            PersonalStatement.objects.filter(institute=previous.institute, app=previous.app).delete()


'''
Function   : On_Additional_Document_Upload 
Description: Create notification, log and sent email on new document upload to application
Parameters : DocumentUpload Instance
Return     : email notification, application log, user notification
'''


@receiver(post_save, sender=DocumentUpload)
def On_Additional_Document_Upload(sender, instance, created, **kwargs):
    # Get Request attribute
    request = get_current_request()
    current_user = request.user
    url_name = '/application/application/%s' % (instance.app.slug)
    MESSAGE = 'Application id %s has some fresh document uploads.' % (
        instance.app.slug)
    log_message = 'Application id %s has some fresh document upload: %s.' % (
        instance.app.slug, instance.name)
    # Create Log
    ApplicationLog.objects.create(type=11, app=instance.app, message=log_message, admin=current_user)
    app_admin = CustomUser.objects.filter(user_type=7)
    # Send notification to App-admin(S)
    for person in app_admin:
        notify.send(instance,
                    recipient=person,
                    description=url_name,
                    target=instance.app,
                    level='info',
                    verb=MESSAGE)
    # Send email
    send_email_notification_for_application(instance.app, MESSAGE)


'''
Function   : On_Additional_Document_Upload 
Description: Create log on delete document on application
Parameters : DocumentUpload Instance
Return     : email notification, application log, user notification
'''


@receiver(pre_delete, sender=DocumentUpload)
def On_Additional_Document_Delete(sender, instance, using, **kwargs):
    # Get Request attribute
    request = get_current_request()
    current_user = request.user
    if instance.app:
        log_message = 'Application id %s has removed document: %s.' % (
            instance.app.slug, instance.name)
        # Create Log
        ApplicationLog.objects.create(type=12, app=instance.app, message=log_message, admin=current_user)


'''
Function   : On_Comment 
Description: Create notification, log and sent email on new comment upload to application
Parameters : ApplicationComment Instance
Return     : email notification, application log, user notification
'''


@receiver(post_save, sender=ApplicationComment)
def On_Comment(sender, instance, created, **kwargs):
    url_name = '/application/application/%s' % (instance.app.slug)
    MESSAGE = 'Application id %s has new comment(s).' % (
        instance.app.slug)
    app_admin = CustomUser.objects.filter(user_type=7)
    # Send notification to App-admin(S)
    for person in app_admin:
        notify.send(instance,
                    recipient=person,
                    description=url_name,
                    target=instance.app,
                    level='info',
                    verb=MESSAGE)
    # Send email
    send_email_notification_for_application(instance.app, MESSAGE)



def update_mentor_profile_link_url_slug(user_slug, name_slug, currently_studying_slug, country_slug, studying_in_slug, url_slug):
    # Mentor Url Slug update
    url = None
    mentors_with_same_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug,
        admin__country_slug=country_slug, url_slug=url_slug)
    temp = []
    # Get list of available user slugs
    for i in mentors_with_same_pi:
        temp.append(i.admin.user_slug)
    # Get mentor object from db1(Database for general information)
    user_mentor = Mentor.objects.get(admin__slug=user_slug)
    if user_mentor.institute:
        matched_cases = Mentor.objects.filter(admin__slug__in=temp,
                                              institute=user_mentor.institute)
    else:
        matched_cases = Mentor.objects.filter(admin__slug__in=temp,
                                              institute_name_slug=user_mentor.institute_name_slug)
    print('matched_cases ', matched_cases.count())
    if matched_cases.count():
        possible_url_slug = ['study-in-' + studying_in_slug, 'study-in-the-' + studying_in_slug,
                             'study-in-' + currently_studying_slug + '-' + studying_in_slug,
                             'study-in-' + currently_studying_slug + '-the-' + studying_in_slug,
                             user_slug, ]
        temp = []
        # Get list of available user slugs
        for i in matched_cases:
            temp.append(i.admin.slug)

        for i in possible_url_slug:
            if MentorPersonalInformation.objects.using('afm_personal_information').filter(
                    admin__user_slug__in=temp,
                    admin__name_slug=name_slug,
                    currently_studying_slug=currently_studying_slug,
                    admin__country_slug=country_slug, url_slug=i).exists():
                pass
            else:
                # print("URL slug: ", i)
                url = i
                break
    return url

'''
Function   : on_mentor_update_profile 
Description: On Mentor successfully update profile notify TAG by an email notification
Parameters : ApplicationComment Instance
Return     : email notification, application log, user notification
'''


@receiver(pre_save, sender=MentorPersonalInformation)
def on_mentor_update_profile(sender, instance: MentorPersonalInformation, **kwargs):
    # Get Request attribute
    if instance.id is not None:
        previous = MentorPersonalInformation.objects.get(id=instance.id)
        if previous.consent4 != instance.consent4:  # field will be updated
            request = get_current_request()
            mail_send_from = MAIL_SEND_FROM
            link = ''.join(['https://', get_current_site(request).domain, '/mentor-profile/', str(instance.admin.user_slug)])
            send_email_notification('Notification from TAG',
                                          'administration/email/mentor_profile_completed.html',
                                          [mail_send_from],
                                          {
                                              'first_name': instance.admin.first_name,
                                              'user_slug': instance.admin.user_slug,
                                              'link': link,
                                          }
                                          )
        if previous.currently_studying_slug != instance.currently_studying_slug \
                or previous.url_slug != instance.url_slug:
            # Create unique url slug for mentor public profile page
            # print("Slug change Action taken")

            url = update_mentor_profile_link_url_slug(instance.admin.user_slug, instance.admin.name_slug,
                                                      instance.currently_studying_slug, instance.admin.country_slug,
                                                      instance.studying_in_slug, instance.url_slug)
            if url:
                instance.url_slug = url


@receiver(pre_save, sender=CustomUserPersonalInformation)
def on_mentor_update_profile_2(sender, instance: CustomUserPersonalInformation, **kwargs):
    # Get Request attribute
    request = get_current_request()
    current_user = request.user
    if hasattr(current_user, 'user_type'):
        if current_user.user_type != 3:
            if instance.id is not None:
                previous = CustomUserPersonalInformation.objects.get(id=instance.id)

                if previous.name_slug != instance.name_slug or previous.country_slug != instance.country_slug:
                    # Create unique url slug for mentor public profile page
                    # print("Slug change Action taken 2")
                    user_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
                        admin__user_slug=instance.user_slug)

                    url = update_mentor_profile_link_url_slug(instance.user_slug, instance.name_slug,
                                                              user_pi.currently_studying_slug, instance.country_slug,
                                                              user_pi.studying_in_slug, user_pi.url_slug)
                    if url:
                        user_pi.url_slug = url
                        user_pi.save()


@receiver(pre_save, sender=Mentor)
def on_mentor_update_profile_3(sender, instance: Mentor, **kwargs):
    # Get Request attribute
    if instance.id is not None:
        previous = Mentor.objects.get(id=instance.id)
        if previous.institute != instance.institute or previous.institute_name_slug != instance.institute_name_slug:
            # Create unique url slug for mentor public profile page
            # print("Slug change Action taken 3")
            user_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
                admin__user_slug=instance.admin.slug)

            # Mentor Url Slug update
            url = None
            mentors_with_same_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
                admin__name_slug=user_pi.admin.name_slug, currently_studying_slug=user_pi.currently_studying_slug,
                admin__country_slug=user_pi.admin.country_slug, url_slug=user_pi.url_slug)
            temp = []
            # Get list of available user slugs
            for i in mentors_with_same_pi:
                temp.append(i.admin.user_slug)
            # print(temp, 'temp mentors_with_same_pi')
            if instance.institute:
                matched_cases = Mentor.objects.filter(admin__slug__in=temp,
                                                      institute=instance.institute)
            else:
                matched_cases = Mentor.objects.filter(admin__slug__in=temp,
                                                      institute_name_slug=instance.institute_name_slug)
            # print(matched_cases, "matched_cases")
            if matched_cases.count():
                print("Condition true")
                possible_url_slug = ['study-in-' + user_pi.studying_in_slug, 'study-in-the-' + user_pi.studying_in_slug,
                                     'study-in-' + user_pi.currently_studying_slug + '-' + user_pi.studying_in_slug,
                                     'study-in-' + user_pi.currently_studying_slug + '-the-' + user_pi.studying_in_slug,
                                     instance.admin.slug, ]
                temp = []
                # Get list of available user slugs
                for i in matched_cases:
                    temp.append(i.admin.slug)

                for i in possible_url_slug:
                    if MentorPersonalInformation.objects.using('afm_personal_information').filter(
                            admin__user_slug__in=temp,
                            admin__name_slug=user_pi.admin.name_slug,
                            currently_studying_slug=user_pi.currently_studying_slug,
                            admin__country_slug=user_pi.admin.country_slug, url_slug=i).exists():
                        pass
                    else:
                        print("URL slug: ", i)
                        url = i
                        break
                if url:
                    user_pi.url_slug = url
                    user_pi.save()