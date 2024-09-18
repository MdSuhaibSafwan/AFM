import operator
from decouple import config
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.db.models.signals import post_save
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.signals import user_logged_in, user_logged_out

from AFM import settings
from AFM.settings import MAIL_SEND_FROM, EMAIL_HOST_USER
from AFM.tasks import send_email_notification
from administration.forms import RegistrationForm, InstituteRegistrationForm, MentorRegistrationForm, \
    MentorPersonalInformationForm, IFGStudentRegistrationForm, \
    StudentPersonalInformationForm, CustomUserPersonalInformationForm, MentorProfileForm, StudentProfileForm, \
    AppAdminRegistrationForm, InstituteUpdateForm, \
    InstituteAdminRegistrationForm, parent_form, update_user_info, UpdateProfilePicForm, \
    InstituteScholarshipForm, SystemMentorRegistrationForm, SystemRecruiterRegistrationForm, LatepointLinkForm, \
    RecruiterRegistrationForm, ContactUsForm, UniversityContactUsForm, MessageMentorForm, MentorBookingLeadsForm, \
    ProfilePhotoForm, MentorUpdateInformationFirstStepForm, MentorUpdateInformationSecondStepForm, MentorConsentForm, \
    MentorPublicProfileCommentForm, TechSupportForm, AdminMeetingLinkForm, MentorUpdateAboutFieldForm, \
    MentorUpdateYoutubeShotsFieldForm, SchoolRegistrationForm, UserRegistrationForm, ApplicantAdditionalQuestionsForm, \
    StudentQuestionsAboutSchool, StudentAdditionalPersonalInformation, FutureStudentInformation, \
    StudentPersonalInformationFirstStepForm, StudentConsentForm, ChatRegistrationForm, \
    StudentProfileStep1Form, StudentQuestionForm, FutureStudentSignupForm
from django.urls import reverse, reverse_lazy
from administration.login_check import super_admin_user_required, parent_admin_user_required, student_user_required, \
    student_parent_admin_user_required, institute_user_required, student_parent_mentor_admin_user_required, \
    mentor_user_required, student_user_complete_profile_required, school_admin_user_required, \
    student_future_student_parent_admin_user_required, future_student_admin_user_required, special_mentor_user_required, \
    future_student_special_mentor_user_required
from administration.models import Mentor, Student, Institute, InstituteAdmin, Parent, Recruiter, CustomUser, \
    BlockUser, InstituteLead, MentorFeedback, AppAdmin, Subscriber, MentorBookingLeads, DemandAndSupply, \
    MentorPublicProfileComment, TechSupport, Admin, ContactUs, School, AdditionalQuestions, FutureStudent, \
    UserCSVImportedData

from administration.templatetags.administration_extras import getsubject, getmentorprofileurl
from blogs.models import Post
from faqs.models import Faq
from application.models import Application, EnglishLanguage, VisaHistory, ApplicationFeedback, Reference, \
    ProfessionalExperience, ProfessionalTrainingCertificate, AcademicQualification, PersonalStatement
from feedback.models import Feedback
from messaging.models import ReportUser, Messaging
from personal_information.models import CustomUserPersonalInformation, MentorPersonalInformation, \
    StudentPersonalInformation, AppBasicInformation, SpokenLanguage, FoundationProvider, AppAddress, \
    AppPassportInformation
from notifications.signals import notify
from administration.filters import MentorFilter, MentorPersonalFilter, RecruiterFilter, TestimonialsFilter, StudentFilter, ParentFilter, \
    MentorBookingLeadsFilter, DemandAndSupplyFilter, TechSupportFilter, ContactUsFilter, StudentSearchFilter, \
    FutureStudentFilter, UserCSVImportedDataFilter
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from smtplib import SMTPException
from django.template import loader
from django.contrib import auth
from django.utils.safestring import mark_safe
from django_countries.fields import CountryField
from webpush import send_user_notification
from django.db.models import Q
from application.forms import ApplicationForm
from bookings.models import UserServices, Appointment
from django.forms import modelformset_factory

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


mail_send_from = MAIL_SEND_FROM
from AFM.settings import SCHOOL_ID

SCHOOL_OBJECT = None
try:
    if SCHOOL_ID:
        SCHOOL_OBJECT = School.objects.get(id=SCHOOL_ID)
except School.DoesNotExist as e:
    print(e)


def clone_data_of_student_table(request):
    queryset = StudentPersonalInformation.objects.using('afm_personal_information').all()
    for element in queryset:
        app_element = AppBasicInformation.objects.using('afm_personal_information').filter(
            user_slug=element.admin.user_slug).first()
        app = Application.objects.filter(admin__slug=element.admin.user_slug).first()
        if app:
            if element.area_of_study and app.subject is None:
                app.subject = element.area_of_study
                app.save()
                print('area_of_study & subject: ', element.area_of_study, ' ', app.subject)
            if element.level_of_english is not None and app.level_of_english is None:
                app.level_of_english = element.level_of_english
                app.save()
                print('level_of_english: ', element.level_of_english, ' ', app.level_of_english)

        if app_element:
            if element.admin.date_of_birth and not app_element.date_of_birth:
                app_element.date_of_birth = element.admin.date_of_birth
                app_element.save()
                print('date_of_birth: ', element.admin.date_of_birth, app_element.date_of_birth)
            if element.admin.gender is not None and app_element.gender is None:
                app_element.gender = element.admin.gender
                app_element.save()
                print('gender: ', element.admin.gender, app_element.gender)
            if element.media_consent and not app_element.media_consent:
                app_element.media_consent = element.media_consent
                app_element.save()
                print('media_consent: ', element.media_consent, app_element.media_consent)
            if element.admin.currently_living_in and not app_element.currently_living_in:
                app_element.currently_living_in = element.admin.currently_living_in
                app_element.save()
                print('currently_living_in: ', element.admin.currently_living_in, ' ', app_element.currently_living_in)
            if element.currently_studying and not app_element.currently_studying:
                app_element.currently_studying = element.currently_studying
                app_element.save()
                print('currently_studying: ', element.currently_studying, ' ', app_element.currently_studying)
            if element.current_or_last_school_name and not app_element.current_or_last_school_name:
                app_element.current_or_last_school_name = element.current_or_last_school_name
                app_element.save()
                print('current_or_last_school_name: ', element.current_or_last_school_name, ' ',
                      app_element.current_or_last_school_name)
            # if element.study_destination and not app_element.study_destination:
            #     app_element.study_destination = element.study_destination
            #     app_element.save()
            #     print('study_destination: ', element.study_destination,' ', app_element.study_destination)
            if element.level_of_english and not app_element.level_of_english:
                app_element.level_of_english = element.level_of_english
                app_element.save()
                print('level_of_english: ', element.level_of_english, ' ', app_element.level_of_english)
            if element.what_are_you_studying and not app_element.what_are_you_studying:
                app_element.what_are_you_studying = element.what_are_you_studying
                app_element.save()
                print('what_are_you_studying: ', element.what_are_you_studying, ' ', app_element.what_are_you_studying)
            if element.last_qualification and not app_element.last_qualification:
                app_element.last_qualification = element.last_qualification
                app_element.save()
                print('last_qualification: ', element.last_qualification, ' ', app_element.last_qualification)
            if element.consent1 and not app_element.consent1:
                app_element.consent1 = element.consent1
                app_element.save()
                print('consent1: ', element.consent1, ' ', app_element.consent1)
    return redirect('administration:home')


def clone_data_of_mobile_field(request):
    queryset = AppBasicInformation.objects.using('afm_personal_information').all()
    for element in queryset:
        if element.mobile and element.mobile_number is None:
            element.mobile_number = element.mobile
            element.save()
            print('Mobile number: ', element.mobile, ' ', element.mobile_number)
    return redirect('administration:home')


def clear_url_slug(request):
    queryset = MentorPersonalInformation.objects.exclude(url_slug=None)
    # queryset = MentorPersonalInformation.objects.filter(admin__user_slug='4v7e6cnq')
    queryset.update(url_slug=None)
    print(queryset, 'queryset')
    return redirect('administration:home')


'''
Function   : Homepage 
Parameters : --
Return     : Redirect to home page
'''


# def home(request):
#     # Check Sessions
#     # print(f"--------------------Session check Home-----------------------")
#     # for key, value in request.session.items():
#     #     print(f"Session-Key: {key} => Session-values: {value}")
#     # print(f"--------------------Session Home Checked-----------------------")
#     # print("Dictionary - ", request.__dict__)
#     # print("------------------------Request-----------------------")
#     if request.user.is_authenticated:
#         return redirect('administration:dashboard')
#     else:
#         return redirect('login')


import random
def home(request):
    domain = get_current_site(request).domain
    print("Domain - ", domain)
    if request.user.is_authenticated:
        return redirect("administration:dashboard")
    
    chat_signup_form = ChatRegistrationForm()
    
    mentorslug_list = []
    mentors = Mentor.objects.filter(profile_status=True).exclude(admin=None)
    for mentor in mentors:
        mentorslug_list.append(mentor.admin.slug)
    print("Mentors slug list - ", mentorslug_list)

    mentors_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(admin__user_slug__in=mentorslug_list)
    if mentors_pi is not None and mentors_pi.count() >= 6:
        mentor_list = list(mentors_pi)
        random_mentors = random.sample(mentor_list,6)
    else:
        random_mentors = []

    students = Student.objects.filter(profile_status=True).exclude(admin=None)
    studentslug_list = []
    for student in students:
        studentslug_list.append(student.admin.slug)
    
    student_pi = StudentPersonalInformation.objects.using('afm_personal_information').filter(admin__user_slug__in=studentslug_list)
    if student_pi is not None and student_pi.count() >= 3:
        student_list = list(student_pi)
        random_students = random.sample(student_list,3)
    else:
        random_students = []

    print("Random Mentors List - ", random_mentors)
    print("Random Students List - ", random_students)

    if request.method == "POST":
        chat_signup_form = ChatRegistrationForm(request.POST)
        if chat_signup_form.is_valid():
            print("chat signup form valid....")
            chat_user = chat_signup_form.save(commit=False)
            chat_user.user_type = 12
            chat_user.is_active = True
            chat_user.save()
            print("Manual Chat Signup based Registration successful - ",chat_user.id, chat_user )
            # Triggers administration signal function(create_user_profile)
            print("Future Student created: ", chat_user.id, chat_user.slug, chat_user.email)
            print("Triggered create_user_profile signal successfully.")        
            print("----------------------Signal successful------------------------")
            
            login(request, chat_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("administration:new_search_alumni")
        else:
            print(chat_signup_form.errors)

    else:
        chat_signup_form = ChatRegistrationForm()        

    return render(request,'administration/home.html',{
        'mentors':mentors,
        'random_mentors':random_mentors,
        'random_students':random_students,
        'form':chat_signup_form
        })




# Added By Areeb
def home_pk(request):
    if request.user.is_authenticated:
        return redirect('administration:dashboard')
    else:
        return render(request, 'website/home_pk.html')


# Added By Areeb
def home_ind(request):
    if request.user.is_authenticated:
        return redirect('administration:dashboard')
    else:
        return render(request, 'website/home_ind.html')


# Added By Areeb
def planner(request):
    if request.user.is_authenticated:
        return redirect('administration:dashboard')
    else:
        return render(request, 'website/planner.html')


def terms_and_conditions(request):  # Done and Tested
    return render(request, 'website/terms-and-conditions.html')


def privacy_notice(request):  # Done and Tested
    return render(request, 'website/privacy-notice.html')


def cookies_policy(request):  # LATER
    return render(request, 'website/cookies-policy.html')


def safeguarding(request):  # Done and Tested
    return render(request, 'website/safeguarding.html')


def online_safety(request):  # Done and Tested
    return render(request, 'website/online-safety.html')


def codes_of_conduct(request):  # Done and Tested
    return render(request, 'website/codes-of-conduct.html')


'''
Function   : page_not_found 
Parameters : --
Return     : Create blank object of CustomUser in respective user object
'''


def page_not_found(request):
    return render(request, "404/404.html")


'''
Function   : check_username_password 
Description: Check if use is authenticated. Only Student, Mentor, Parent, Institute & Admin are allowed to login
Parameters : username & password, receive by GET method from login form.
Return     : JSON Message
'''


def check_username_password(request):
    message = ''
    if request.method == 'GET':
        username = request.GET['email']
        password = request.GET['password']
        user_obj = CustomUser.objects.filter(username=username).first()
        user = auth.authenticate(username=username, password=password, is_active__in=[True, False])
        if user:
            message_user_already_exist = "Your account already exists on ApplyforUniversity.<br> Please <a href='" \
                                         + config('AFU_LINK') + "/accounts/login/" + \
                                         "' target='_blank' ><b>click here</b></a> to login."
            # Only Student, Mentor, Parent, Institute, Future Student & Admin are allowed to login
            if user.user_type not in [0, 3, 4, 5, 11, 12]:
                message = 'Please enter a correct username and password.</br> Note that both fields may be ' \
                          'case-sensitive. '       
        else:
            message = 'Please enter a correct username and password.</br> Note that both fields may be case-sensitive.'
        if user_obj is not None and user_obj.is_active == False:
            message = 'Your account is not activated. Please check your Inbox and click on the link provided to ' \
                      'activate your account.'
    return JsonResponse({'message': message, })


'''
Function   : change_password 
Description: Change user name password from dashboard
Parameters : PasswordChangeForm form.
Return     : Redirect to dashboard with a massage
'''


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('administration:dashboard')
        else:
            for i in form.errors:
                if i == "old_password":
                    messages.error(
                        request, 'Your old password was entered incorrectly. Please enter it again.')
                if i == "new_password2":
                    messages.error(
                        request, 'The two password fields didn’t match.')
    return redirect('administration:dashboard')


'''
Function   : get_email_exists 
Description: Check if email is already registered in the system
Parameters : -
Return     : JsonResponse with boolean data
'''


def get_email_exists(request):
    if request.method == 'GET':
        email_exist = False
        email = request.GET['email']

        if CustomUser.objects.filter(email__iexact=email).exists():
            email_exist = True

        return JsonResponse({"email_exist": email_exist})


'''
Function   : get_email_exists_on_afu 
Description: Check if email is already registered on Applyforuniversity
Parameters : -
Return     : JsonResponse with boolean data as email_exist and message text as message_user_already_exist
'''


def get_email_exists_on_afu(request):
    if request.method == 'GET':
        email_exist = False
        email = request.GET['email']
        message_user_already_exist = ""
        if CustomUser.objects.filter(email=email).exists():
            user_object = CustomUser.objects.filter(email=email).first()
            if MentorPersonalInformation.objects.using('afm_personal_information').filter(
                    admin__user_slug=user_object.slug).exclude(currently_studying=6).exists() or \
                    Application.objects.filter(admin__slug=user_object.slug).first().subject != 6:
                # StudentPersonalInformation.objects.using('afm_personal_information').filter(
                #     admin__user_slug=user_object.slug).exclude(area_of_study=6).exists():
                email_exist = True
                # message_user_already_exist = "Your account already exists on ApplyforUniversity.<br> Please <a href='" \
                #                              + config('AFU_LINK') + "/accounts/login/" + \
                #                              "' target='_blank' ><b>click here</b></a> to login."

        return JsonResponse({"email_exists_on_afu": email_exist, "message": message_user_already_exist})


'''
Function   : check_profile_password 
Description: Check if user has entered correct password
Parameters : -
Return     : JsonResponse with boolean data 
'''


def check_profile_password(request):
    password_confirm = False
    if request.method == 'GET':
        old_password = request.GET['password']
        if request.user.check_password(old_password) == True:
            # Apply whatever logic you want to apply
            password_confirm = True
    return JsonResponse({"password_confirm": password_confirm})


'''
Function   : select_user_type 
Description: When user has not selected his/her user type or database has NULL value for user's user type then 
             User will redirected to this view and has to select user type Applicant/Parent.
Parameters : --
Return     : Redirect to update profile form
'''


@login_required
def select_user_type(request):
    context = {}
    # Check Sessions
    for key, value in request.session.items():
        print(f"--------------------Session Analysis-----------------------")
        print(f"Session-Key: {key} => Session-values: {value}")
    
    if 'chatslug' in request.session:
        context['chatslug'] = request.session['chatslug']

    # If user already has a user type they will be redirected to his/her respective dashboard.
    if request.user.user_type is not None:
        return redirect('administration:dashboard')
    
    if request.method == 'POST':
        user_type = request.POST['user_type']
        request.user.user_type = int(user_type)
        request.user.save()
        print("User Type -", user_type)
        super_admin = CustomUser.objects.filter(user_type=0)
        
        # If user type is Student create Null objects for relative models
        if request.user.user_type == 3:
            Student.objects.create(admin=request.user, school=SCHOOL_OBJECT)
            user = CustomUserPersonalInformation.objects.using('afm_personal_information').create(
                user_slug=request.user.slug,
                first_name=request.user.first_name,
                last_name=request.user.last_name)
            StudentPersonalInformation.objects.using('afm_personal_information').create(admin=user)
            app = Application.objects.create(admin=request.user)
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
                                                                                          user_slug=request.user.slug,
                                                                                          first_name=request.user.first_name,
                                                                                          surname=request.user.last_name,
                                                                                          email=request.user.email)
            AppAddress.objects.using('afm_personal_information').create(app=app_pi)
            AppPassportInformation.objects.using('afm_personal_information').create(app=app_pi)
            url_name = '#'
            verb = 'New Student registered as %s' % request.user.first_name
            for person in super_admin:
                # Send notification to super-admin(S)
                notify.send(request.user,
                            recipient=person,
                            description=url_name,
                            target=request.user,
                            level='info',
                            verb=verb)

        # If user is a Mentor
        elif request.user.user_type == 4:
            Mentor.objects.create(admin=request.user, school=SCHOOL_OBJECT)
            user = CustomUserPersonalInformation.objects.using('afm_personal_information').create(
                user_slug=request.user.slug,
                first_name=request.user.first_name,
                last_name=request.user.last_name)
            MentorPersonalInformation.objects.using('afm_personal_information').create(admin=user)

            url_name = '#'
            verb = 'New Mentor registered as %s' % request.user.first_name
            # Send super-admin notification
            for person in super_admin:
                notify.send(request.user,
                            recipient=person,
                            description=url_name,
                            target=request.user,
                            level='info',
                            verb=verb)

        # If user type is Parent create Null objects for relative models
        elif request.user.user_type == 5:
            Parent.objects.create(admin=request.user)
            url_name = '#'
            verb = 'New Parent registered as %s' % request.user.first_name
            for person in super_admin:
                # Send notification to super-admin(S)
                notify.send(request.user,
                            recipient=person,
                            description=url_name,
                            target=request.user,
                            level='info',
                            verb=verb)

        # If user is a Future Student
        elif request.user.user_type == 12:
            FutureStudent.objects.create(admin=request.user, school=SCHOOL_OBJECT)
            url_name = '#'
            verb = 'New Future Student registered as %s' % request.user.first_name
            for person in super_admin:
                # Send notification to super-admin(S)
                notify.send(request.user,
                            recipient=person,
                            description=url_name,
                            target=request.user,
                            level='info',
                            verb=verb)

        else:
            logout(request)
            messages.error(request, "Failed to update user, Please login again!")
            return HttpResponseRedirect(reverse("login"))
    
        return redirect('administration:dashboard')
    
    else:
        return render(request, 'administration/select_user_type.html', context)


'''
Function   : registration
Description: Register Student/Parent user and sent verification email
Parameters : --
Return     : Create Student / Parent user
'''


def registration(request, mentor_slug=''):
    form = RegistrationForm()
    if request.method != "POST":
        return render(request, 'registration/registration.html', {'form': form, 'mentor_slug': mentor_slug})
    else:
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            student = user_form.save(commit=False)
            student.is_active = False
            student.save()
            print("CustomUser type - ", student, student.user_type)
            # Triggers administration signal function(create_user_profile)
            print("Student created: ", student.id, student.slug, student.email)
            print("Triggered create_user_profile signal successfully.")        
            print("----------------------Signal successful------------------------")
            
            # Sent email for verification
            base_link = request.POST.get('link')
            mentor_slug = request.POST.get('mentor_slug')
            print(base_link, mentor_slug)
            if mentor_slug:
                # Will redirect to mentor comment page
                link = f"{base_link}/confirmAccount/{student.slug}/{mentor_slug}"
            else:
                link = f"{base_link}/confirmAccount/{student.slug}"

            print(link, " - Confirm Account link")

            # Send Email: Applicant/Parent/Mentor
            subject = 'Account confirmation - International Foundation Group'
            email_template = 'administration/email/verification.html'
            email_data = {'link': link,'first_name': student.first_name + student.last_name,}
            context = {
                "first_name": f"{student.first_name} {student.last_name}",
                "link":link
            }
            html_message = render_to_string(email_template, context)
            plain_message = strip_tags(html_message)

            # Celery Email:
            # send_email_notification.delay(subject, email_template, [student.email,],email_data)

            try:  
                msg = EmailMultiAlternatives(
                                subject = subject, 
                                body = plain_message,
                                from_email =  settings.EMAIL_HOST_USER,
                                to= [student.email,]
                                )

                msg.attach_alternative(html_message, "text/html")
                msg.send()
                print("E-mail sent successfully.")
                messages.success(
                    request, "Please check your Inbox and click on the link provided to activate your account")
            except Exception as e:
                print("E-mail Error: ",e)
                messages.error(
                    request, "Apologies, but due to a system upgrade you are unable to register - please "
                                        "try again in about 24 hours.")
                
            return redirect('login')
        else:
            print(user_form.errors)
            messages.error(request, "Failed to update your request, Please try again.")
            return render(request, "registration/registration.html", {'form': user_form})


'''
Author     : Viral Solanki 
Date       : 12/17/2020 
Function   : Register Mentor 
Parameters : --
Return     : Mentor user
'''

def former_student_registration(request):
    form = MentorRegistrationForm
    if request.method != "POST":
        return render(request, 'registration/former_student_registration.html', {'form': form})
    else:
        form = MentorRegistrationForm(request.POST)
        if form.is_valid():
            mentor = form.save(commit=False)
            mentor.user_type = 4
            mentor.is_active = False
            mentor.save()
            print("CustomUser type - ", mentor, mentor.user_type)
            print("Triggered create_user_profile signal successfully.")        
            print("----------------------Signal successful------------------------")
            
            # Sent email for verification
            base_link = request.POST.get('link')
            mentor_slug = request.POST.get('mentor_slug')
            print(base_link, mentor_slug)
            if mentor_slug:
                # Will redirect to mentor comment page
                link = f"{base_link}/confirmAccount/{mentor.slug}/{mentor_slug}"
            else:
                link = f"{base_link}/confirmAccount/{mentor.slug}"

            print("Confirm Account Email link - ", link)

            # Send Email: Applicant/Parent/Mentor
            subject = 'Account confirmation - International Foundation Group'
            email_template = 'administration/email/verification.html'
            email_data = {'link': link,'first_name': mentor.first_name + mentor.last_name,}
            context = {
                "first_name": f"{mentor.first_name} {mentor.last_name}",
                "link":link
            }
            html_message = render_to_string(email_template, context)
            plain_message = strip_tags(html_message)

            # Celery Email:
            # send_email_notification.delay(subject, email_template, [student.email,],email_data)

            try:  
                msg = EmailMultiAlternatives(
                                subject = subject, 
                                body = plain_message,
                                from_email =  settings.EMAIL_HOST_USER,
                                to= [mentor.email,]
                                )

                msg.attach_alternative(html_message, "text/html")
                msg.send()
                print("E-mail sent successfully.")
                messages.success(
                    request, "Please check your Inbox and click on the link provided to activate your account")
            except Exception as e:
                print("E-mail Error: ",e)
                messages.error(
                    request, "Apologies, but due to a system upgrade you are unable to register - please "
                                        "try again in about 24 hours.")
                
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request, "Failed to update your request, Please try again.")
            return render(request, "registration/former_student_registration.html", {'form':form})
        



def current_student_registration(request):
    form = IFGStudentRegistrationForm()
    if request.method != "POST":
        return render(request, 'registration/current_student_registration.html', {'form': form})
    else:
        form = IFGStudentRegistrationForm(request.POST)
        if form.is_valid():
            ifgstudent = form.save(commit=False)
            ifgstudent.user_type = 3
            ifgstudent.is_active = False
            ifgstudent.save()
            print("CustomUser type - ", ifgstudent, ifgstudent.user_type)
            print("Triggered create_user_profile signal successfully.")        
            print("----------------------Signal successful------------------------")
            
            # Sent email for verification
            base_link = request.POST.get('link')
            mentor_slug = request.POST.get('mentor_slug')
            print(base_link, mentor_slug)
            if mentor_slug:
                # Will redirect to mentor comment page
                link = f"{base_link}/confirmAccount/{ifgstudent.slug}/{mentor_slug}"
            else:
                link = f"{base_link}/confirmAccount/{ifgstudent.slug}"

            print("Confirm Account Email link - ", link)

            # Send Email: Applicant/Parent/Mentor
            subject = 'Account confirmation - International Foundation Group'
            email_template = 'administration/email/verification.html'
            email_data = {'link': link,'first_name': ifgstudent.first_name + ifgstudent.last_name,}
            context = {
                "first_name": f"{ifgstudent.first_name} {ifgstudent.last_name}",
                "link":link
            }
            html_message = render_to_string(email_template, context)
            plain_message = strip_tags(html_message)
            
            # Celery Email:
            # send_email_notification.delay(subject, email_template, [student.email,],email_data)
            
            try:  
                msg = EmailMultiAlternatives(
                                subject = subject, 
                                body = plain_message,
                                from_email =  settings.EMAIL_HOST_USER,
                                to= [ifgstudent.email,]
                                )

                msg.attach_alternative(html_message, "text/html")
                msg.send()
                print("E-mail sent successfully.")
                messages.success(
                    request, "Please check your Inbox and click on the link provided to activate your account")
            except Exception as e:
                print("E-mail Error: ",e)
                messages.error(
                    request, "Apologies, but due to a system upgrade you are unable to register - please "
                                        "try again in about 24 hours.")
                
            return redirect('login')
        else:
            print(form.errors)
            messages.error(request, "Failed to update your request, Please try again.")
            return render(request, "registration/current_student_registration.html", {'form':form})








'''
Function   : redirect_registration
Description: Redirect to registration
Parameters : --
Return     : Redirect to registration
'''


def redirect_registration(request):
    return redirect('administration:registration')


'''
Function   : confirmAccount
Description: Verify user from verification link in email
Parameters : --
Return     : User Verified
'''


def confirmAccount(request, slug, mentor_slug=''):
    # Get appointment link
    admin_user_links = Admin.objects.first()
    appointment_link = '/contact/'
    if admin_user_links.appointment_link:
        appointment_link = admin_user_links.appointment_link
    print("Appointment Link -", appointment_link)

    obj = CustomUser.objects.get(slug=slug)
    if not (obj.is_active):
        obj.is_active = True
        obj.save()
        link = config('AFM_LINK') + "/accounts/login/"
        msg = ''

        # # Check if user is current student at IFG
        # if obj.user_type == 3:
        #     pass # Current Student Logic

        # Check if user is mentor
        if obj.user_type == 4:
            msg = "You are just a few steps to having your profile made visible to potential applicants and " \
                  "mentees around the world."
        send_email_notification.delay('Please complete your profile',
                                'administration/email/complete_your_profile.html', [obj.email],
                                {'link': link, 'msg': msg})
        # Check if user is mentor
        # if obj.user_type == 4:
        #     msg = 'Your email address has been verified.<br>' \
        #           'If you have any queries in completing your profile, please ' \
        #           '<a href="{}" target="_blank"><u>click ' \
        #           'here</u></a> to book an appointment with our onboarding team.<br>' \
        #           'They will also be able to provide further details and opportunities that TAG can offer you.'.format(
        #         appointment_link)
        #     messages.success(request, mark_safe(msg))
        # else:
        #     messages.success(request,
        #                      mark_safe('Your email address has been verified successfully....'))
        login(request, obj, backend='django.contrib.auth.backends.ModelBackend')

        # Mentor slug in request
        if mentor_slug:
            if obj.user_type == 3:
                # return redirect('administration:update_profile_twfl', mentor_slug)
                return redirect('administration:dashboard')
            if obj.user_type == 5:
                return redirect('administration:update_parent_profile_twfl', mentor_slug)
        return redirect('login')
    else:
        # Check if user is mentor
        if obj.user_type == 4:
            msg = 'Your email address has already been verified.'
            messages.error(request, mark_safe(msg))
        else:
            messages.error(request,
                           mark_safe('Your email address has already been verified.'))
    return redirect('login')


'''
Author     : Viral Solanki 
Date       : 12/17/2020 
Function   : Register App-admin
Parameters : --
Return     : App-admin  user
'''


@super_admin_user_required
def app_admin_registration(request):
    title = 'App Admin'
    if request.method != "POST":
        form = UserRegistrationForm
        return render(request, 'administration/admin/app_admin_registration.html', {'form': form, 'title': title})
    else:
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # try:
            app_admin = user_form.save(commit=False)
            # app_admin.user_type = 7
            app_admin.save()

            messages.success(request, "Successfully Registered")
            return redirect('administration:list_app_admin_twfl')
        else:
            print(user_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "administration/admin/app_admin_registration.html", {'form': user_form, 'title': title})


@super_admin_user_required
def user_registration(request):
    title = 'User Registration'
    if request.method != "POST":
        form = UserRegistrationForm
        return render(request, 'administration/admin/app_admin_registration.html', {'form': form, 'title': title})
    else:
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # try:
            app_admin = user_form.save(commit=False)
            app_admin.save()

            messages.success(request, "Successfully Registered")
            return redirect('administration:list_app_admin_twfl')
        else:
            print(user_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "administration/admin/app_admin_registration.html", {'form': user_form, 'title': title})


'''
Author     : Viral Solanki 
Date       : 12/17/2020 
Function   : Register Institute 
Parameters : --
Return     : Institute user
'''


@super_admin_user_required
def institute_registration_twfl(request):
    if request.method != "POST":
        form = InstituteRegistrationForm
        form2 = InstituteScholarshipForm
        # scholarship_formset = modelformset_factory(Institute_scholarship_programme, form=institute_scholarship_form,
        #                                                   extra=1,
        #                                                   max_num=3)
        return render(request, 'registration/institute_registration.html', {'form': form, 'form2': form2})
    else:
        user_form = InstituteRegistrationForm(request.POST)
        user_form2 = InstituteScholarshipForm(request.POST, request.FILES)

        if user_form.is_valid() and user_form2.is_valid():
            # try:
            institute = user_form.save(commit=False)
            institute.user_type = 2
            institute.save()
            institute = Institute.objects.get(admin=institute)
            institute.institute_name = user_form2.cleaned_data['institute_name']
            # institute.country = user_form2.cleaned_data['country']
            institute.save()
            user_form2 = InstituteScholarshipForm(
                request.POST, request.FILES, instance=institute)
            user_form2.save()
            FoundationProvider.objects.using('afm_personal_information').create(
                foundation_provider=institute.institute_name)

            messages.success(request, "Successfully Registered")
            return redirect('administration:list_institutes_twfl')
        else:
            print(user_form.errors)
            print(user_form2.errors)
            messages.error(request, "Failed to register, Form is not valid")
            return render(request, "registration/institute_registration.html", {'form': user_form, 'form2': user_form2})





'''
Function   : dashboard
Description: User Dashboard after successful login
Parameters : --
Return     : Dashboard page for user
'''


@login_required
def dashboard(request):
    # Check Sessions
    print(f"--------------------Session Check Dashboard-----------------------")
    for key, value in request.session.items():
        print(f"Session-Key: {key} => Session-values: {value}")
    print(f"--------------------Session Analysis Checked-----------------------")
    current_user = request.user
    total_feedback = Feedback.objects.filter(user=request.user)
    print(F"Request User - {current_user}, Usertype - {current_user.user_type}")

    # If user is Super Admin
    if current_user.user_type == 0:
        admin_user = Admin.objects.first()
        meeting_form = AdminMeetingLinkForm(instance=admin_user or None)
        return render(request, 'administration/dashboard.html', {'meeting_form': meeting_form})

    # IF user type is unknown
    elif current_user.user_type is None:
        return redirect('administration:select_user_type')

    elif current_user.user_type not in [3, 4, 5, 11, 12, None]:
        logout(request)
        messages.error(request, "Failed to Login")

    # If user is Admin
    elif current_user.user_type == 1:
        return render(request, 'administration/dashboard.html', )

    # If user is School
    elif current_user.user_type == 11:
        return render(request, 'administration/dashboard.html', )
    # If user is System Mentor
    # elif current_user.user_type == 9:
    #     return redirect('chat')
    
    # If user is Institute
    elif current_user.user_type == 2:
        institute_instance = Institute.objects.get(admin=request.user)
        requested_applications = institute_instance.selected_institutes.filter(status=0).count()
        my_applications = institute_instance.institute.all().count()
        total_applications = Application.objects.filter(status=0).count()
        mentors = Mentor.objects.all().count()
        mentors_list = Mentor.objects.all().order_by('-id')[:4]
        temp = []
        for i in mentors_list:
            temp.append(i.admin.slug)
        pi_info = MentorPersonalInformation.objects.using('afm_personal_information').filter(admin__user_slug__in=temp)

        return render(request, "administration/dashboard.html",
                      {'institute_instance': institute_instance, 'my_applications': my_applications,
                       'requested_applications': requested_applications, 'total_applications': total_applications,
                       'mentors': mentors, 'mentors_list': mentors_list,
                       'pi_info': pi_info})
    
    # If user is Current Student at IFG
    elif current_user.user_type == 3:
        stud_mentor = Student.objects.get(admin=request.user)
        if stud_mentor.school != SCHOOL_OBJECT:
            messages.error(request, "Failed to Login")
            logout(request)
            return redirect('login')

        pi_user = StudentPersonalInformation.objects.using('afm_personal_information').get(
            admin__user_slug=request.user.slug)
        
        if not pi_user.consent1:
            print("------------------------- First Complete Profile -------------------------")
            return redirect('administration:current_student_profile_step_1')

        app = Application.objects.filter(admin=request.user, status__in=[0, 1, 2]).first()
        print("-------------------Dashboard------------------")
        print("Student Personal Information - ", pi_user)
        print("Application - ", app)
        return redirect('administration:new_search_alumni')
    
    # If user is Mentor
    elif current_user.user_type == 4:
        user_mentor = Mentor.objects.get(admin=request.user)
        if user_mentor.school != SCHOOL_OBJECT:
            messages.error(request, "Failed to Login")
            logout(request)
            return redirect('login')
        faq_list = Faq.objects.filter(user_type__in=[4, 0], status='publish').order_by('rank')
        pi_user = MentorPersonalInformation.objects.using(
            'afm_personal_information').get(admin__user_slug=request.user.slug)

        if not pi_user.consent4:
            return redirect('administration:upload_public_information_twfl')
        else:

            students = user_mentor.student_set.all()
            total_students = Student.objects.all().count()
            total_feedback = MentorFeedback.objects.filter(
                mentor=user_mentor).count()
            total_blogs = Post.objects.filter(author=request.user.mentor).count()
            total_services = UserServices.objects.filter(provider_id=user_mentor.admin.id).count()
            total_appointments = Appointment.objects.filter(provider=request.user).count()
            total_services = UserServices.objects.filter(provider_id=user_mentor.admin.id).count()
            temp = []
            for i in students:
                temp.append(i.admin.slug)
            pi_info = StudentPersonalInformation.objects.using(
                'afm_personal_information').filter(admin__user_slug__in=temp)
            return render(request, 'administration/dashboard.html',
                          {'students': students, 'personal_info_list': pi_info, 'total_students': total_students,
                           'total_feedback': total_feedback,
                           'total_blogs': total_blogs,
                           'faq_list': faq_list,
                           'total_services': total_services,
                           'total_appointments': total_appointments,
                           })
    
    # If user is Parent
    elif current_user.user_type == 5:
        parent = Parent.objects.get(admin__id=request.user.id)
        if parent.country is None or parent.country == '':
            return redirect('administration:update_parent_profile_twfl')
        return redirect('administration:new_search_alumni')

    # If user is Future Student
    elif current_user.user_type == 12:
        future_student = FutureStudent.objects.get(admin=request.user)
        if future_student.school != SCHOOL_OBJECT:
            messages.error(request, "Failed to Login")
            logout(request)
            return redirect('login')
        return redirect('administration:new_search_alumni')

    else:
        logout(request)
        messages.error(request, "Failed to Login")
        return HttpResponseRedirect(reverse("login"))


'''
Function   : delete_profile_pic 
Description: Delete User's profile pic
Parameters : user slug
Return     : Redirect to update profile page
'''


@login_required
def delete_profile_pic(request, slug):
    # Check if user is Mentor
    if request.user.user_type == 4:
        # Get Mentor object from personal information database to delete profile photo
        pic = CustomUserPersonalInformation.objects.get(user_slug=slug)
        pic.profile_pic.delete()
    else:
        pic = CustomUser.objects.get(slug=slug)
        pic.profile_pic.delete()
    return redirect('administration:update_profile_twfl')


'''
Function   : update_profile_pic 
Description: Update User's profile pic
Parameters : user slug
Return     : Redirect to update profile page
'''


@login_required
def update_profile_pic(request, pk):
    user = CustomUser.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateProfilePicForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            # Check if user is Parent
            if request.user.user_type == 5:
                return redirect('administration:update_parent_profile_twfl')
    return redirect('administration:update_profile_twfl')


# ----------------------------------------------------------------
# PARENT MODULES
# ----------------------------------------------------------------

'''
Date       : 12/20/2020 
Function   : update profile 
Description: user have to fill all the profile details to continue
Parameters : --
Return     : updated profile and redirect to dashboard
'''


@parent_admin_user_required
def update_parent_profile_twfl(request, mentor_slug=''):
    parent_instance = Parent.objects.get(admin=request.user)

    if request.method != 'POST':
        user_form = update_user_info(instance=request.user)
        parent_user_form = parent_form(instance=parent_instance)
        return render(request, 'administration/parent/update_profile.html',
                      {'form': user_form, 'form2': parent_user_form, 'parent_instance': parent_instance})

    else:
        user_form = update_user_info(
            request.POST, request.FILES, instance=request.user)
        parent_user_form = parent_form(request.POST, instance=parent_instance)

        if user_form.is_valid() and parent_user_form.is_valid():
            user_form.save()
            parent_user_form.save()
            messages.success(request, "Profile Successfully Updated ")
            if mentor_slug:
                return redirect('messaging:comment_mentor_public_profile_twfl', mentor_slug)
            return HttpResponseRedirect(reverse("administration:dashboard"))

        else:
            messages.error(
                request, "Failed to Update Profile form is not valid")
            return render(request, 'administration/parent/update_profile.html',
                          {'form': user_form, 'form2': parent_user_form, 'parent_instance': parent_instance,
                           'pic_form': UpdateProfilePicForm()})


# ----------------------------------------------------------------
# STUDENT MODULES
# ----------------------------------------------------------------

'''
Function   : update_profile_twfl 
Description: Update profile for Student & Mentor
Parameters : --
Return     : Redirect to update profile page
'''


@login_required
def update_profile_twfl(request, mentor_slug=''):
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    custom_user_pi_form = CustomUserPersonalInformationForm(instance=pi_user)
    if request.method != 'POST':
        user_form = StudentProfileForm(
            instance=Student.objects.get(admin=request.user))
        student_pi_instance = StudentPersonalInformation.objects.using(
            'afm_personal_information').get(admin=pi_user)
        user_pi_form = StudentPersonalInformationForm(instance=student_pi_instance)
        # Check if user has already completed their profile by checking any of the required field is None.
        if pi_user.gender is None:
            messages.success(request,
                             "Welcome to International Foundation Group, Please complete your profile below.")
        return render(request, 'administration/student/update_profile.html',
                      {'form': user_pi_form, 'form2': custom_user_pi_form, 'form3': user_form,
                       'pic_form': UpdateProfilePicForm(), 'pi_user': pi_user})
    else:
        custom_user_pi_form = CustomUserPersonalInformationForm(
            request.POST, request.FILES, instance=pi_user)
        student_pi_instacnce = StudentPersonalInformation.objects.using(
            'afm_personal_information').get(admin=pi_user)
        user_pi_form = StudentPersonalInformationForm(
            request.POST, request.FILES, instance=student_pi_instacnce)
        user_form = StudentProfileForm(
            request.POST, instance=Student.objects.get(admin=request.user))
        if user_pi_form.is_valid() and custom_user_pi_form.is_valid() and user_form.is_valid():
            post = user_pi_form.save(commit=False)
            post.save(using="afm_personal_information")
            user_pi_form.save_m2m()
            custom_user_pi_form.save()
            user_form.save()
            messages.success(request, "Profile Successfully Updated ")
            if mentor_slug:
                return redirect('administration:comment_mentor_public_profile_twfl', mentor_slug)
            # return redirect("administration:my_profile", request.user.slug)
            if request.user.application.all().first().status is None:
                messages.success(request, "Please complete your application form")
                return redirect("application:application_consent_twfl", request.user.application.all().first().slug)
            return redirect("administration:dashboard")
        else:
            messages.error(request, "Failed to Update Profile form is not valid")

            return render(request, 'administration/student/update_profile.html',
                          {'form': user_pi_form, 'form2': custom_user_pi_form, 'form3': user_form,
                           'pic_form': UpdateProfilePicForm(), 'pi_user': pi_user})


'''
Date       : 12/16/2020 
Function   : Search mentors 
Description: Display all the mentors available, student can select his/her mentors
Parameters : --
Return     : mentors list with details
'''


@student_user_required
def default_search_twfl(request, user_slug):
    queryset = StudentPersonalInformation.objects.using(
        'afm_personal_information').get(admin__user_slug=user_slug)
    link = '/search-mentors?'
    # create default search url based on user profile
    # Check if user has selected any languages
    if queryset.admin.spoken_languages.first():
        for i in queryset.admin.spoken_languages.all():
            link += 'admin__spoken_languages=' + str(i.id) + '&'
    link += 'currently_studying=' + str(queryset.area_of_study)
    link += '&admin__country=GB'

    if queryset.study_destination:
        for i in queryset.study_destination:
            link += '&studying_in_countries=' + i.code
    return redirect(link)


@student_future_student_parent_admin_user_required
def search_mentors_twfl(request):
    # from datetime import timedelta
    # from django.utils import timezone
    # queryset = MentorPersonalInformation.objects.using(
    #     'afm_personal_information').filter(
    #     Q(consent4=None) | Q(consent4=False),
    #     admin__created_at__lt=(timezone.now() - timedelta(hours=48)),
    #         admin__created_at__gt=(timezone.now() - timedelta(hours=72)), ).order_by('created_at')
    # print(queryset)
    # Exclude reported users

    reported_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                               is_removed=False).values_list('reported_user')
    # Exclude users from which current user get reported from
    reported_by_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                  is_removed=False).values_list('report_by_user')
    mentors = Mentor.objects.filter(
        admin__is_active=True,
        profile_status=True,
        school=SCHOOL_OBJECT).exclude(Q(admin__id__in=reported_users) | Q(admin__id__in=reported_by_users), )
    temp = []
    for i in mentors:
        if i.admin.slug and i.admin.slug not in temp:
            temp.append(i.admin.slug)
    # Get Mentors object of personal_information database with currently_studying as Medicine
    queryset = MentorPersonalInformation.objects.using(
        'afm_personal_information').filter(admin__user_slug__in=temp).order_by('id')
    # Apply filter
    filtered_qs = MentorFilter(request.GET, queryset)
    # Apply Pagination
    paginated_filtered = Paginator(filtered_qs.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    about_me_form = None
    additional_questions_formset = None
    basic_info = None
    questions_about_school_form = None
    student_additional_personal_information_form = None
    student_obj = None
    future_student_info_form = None
    if request.user.user_type == 3:
        student_obj = Student.objects.get(
            admin__slug=request.user.slug)

        # if not AdditionalQuestions.objects.filter(student=student_obj).exists():
        #     AdditionalQuestions.objects.bulk_create(
        #         [AdditionalQuestions(student=student_obj),
        #          AdditionalQuestions(student=student_obj),
        #          AdditionalQuestions(student=student_obj)])

        app = Application.objects.get(admin=request.user)
        basic_info = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id,
                                                                                       user_slug=request.user.slug)
        additional_questions_formset = modelformset_factory(AdditionalQuestions, form=ApplicantAdditionalQuestionsForm,
                                                            extra=3,
                                                            # can_delete=True
                                                            )

        questions_about_school_form = StudentQuestionsAboutSchool(instance=student_obj)
        about_me_form = ApplicationForm(instance=basic_info)
        student_additional_personal_information_form = StudentAdditionalPersonalInformation(instance=basic_info)

        if request.method == "POST":
            if 'form1_submit' in request.POST:
                about_me_form = ApplicationForm(request.POST, instance=basic_info)
                additional_questions_form = additional_questions_formset(request.POST, request.FILES,
                                                                         queryset=AdditionalQuestions.objects.filter(
                                                                             student=student_obj))

                if about_me_form.is_valid() and additional_questions_form.is_valid():
                    for instance in additional_questions_form:
                        obj = instance.save(commit=False)
                        if obj.q1:
                            obj.student = student_obj
                            obj.save()
                    obj2 = about_me_form.save(commit=False)
                    obj2.save()
                    print("About me - ", obj2)
                    print("Form1 submitted successfully....")
                else:
                    messages.error(request, "Invalid Form")
        
            if 'form2_submit' in request.POST:
                questions_about_school_form = StudentQuestionsAboutSchool(request.POST, instance=student_obj)
                student_additional_personal_information_form = StudentAdditionalPersonalInformation(request.POST,
                                                                                                    instance=basic_info)
                if questions_about_school_form.is_valid() and student_additional_personal_information_form.is_valid():
                    questions_about_school_form.save()
                    student_additional_personal_information_form.save()
                    print("Form2 submitted successfully....")


        # else:
        #     additional_questions_formset = additional_questions_formset(
        #         queryset=AdditionalQuestions.objects.filter(student=student_obj))

    if request.user.user_type == 12:
        student_obj = FutureStudent.objects.get(
            admin__slug=request.user.slug)
        print("Future Student - ", student_obj)
        # future_student_info_form = FutureStudentInformation(instance=student_obj)
        # if request.method == "POST":
        #     future_student_info_form = FutureStudentInformation(request.POST, instance=student_obj)
        #     if future_student_info_form.is_valid():
        #         future_student_info_form.save()

    return render(request, 'administration/student/search_mentors.html',
                  {'mentors': mentors, 'personal_info_list': page_obj, 'form': filtered_qs.form,
                   'page_obj': page_obj, 'form1': about_me_form, 'formset': additional_questions_formset,
                   'form3': questions_about_school_form,
                   'form5': student_additional_personal_information_form,
                   'form4': future_student_info_form,
                   'basic_info': basic_info, 'student': student_obj})




def new_search_all(request):
    reported_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                               is_removed=False).values_list('reported_user')
    # Exclude users from which current user get reported from
    reported_by_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                  is_removed=False).values_list('report_by_user')
    students = Student.objects.filter(
        admin__is_active=True,
        school=SCHOOL_OBJECT).exclude(Q(admin__id__in=reported_users) | Q(admin__id__in=reported_by_users))
    student_slugs = []
    for i in students:
        if i.admin.slug and i.admin.slug not in student_slugs:
            student_slugs.append(i.admin.slug)
    print("student slugs - ", student_slugs)
    # Get Filters for Mentor object from personal_information database.
    students_pi = StudentPersonalInformation.objects.using(
        'afm_personal_information').filter(admin__user_slug__in=student_slugs).order_by('id')
      
    mentors = Mentor.objects.filter(
        admin__is_active=True,profile_status=True,
        school=SCHOOL_OBJECT).exclude(Q(admin__id__in=reported_users) | Q(admin__id__in=reported_by_users), )
    mentor_slugs =[]
    for i in mentors:
        if i.admin.slug and i.admin.slug not in mentor_slugs:
            mentor_slugs.append(i.admin.slug)
    
    # Get Filters for Mentor object from personal_information database.
    mentors_pi = MentorPersonalInformation.objects.using(
        'afm_personal_information').filter(admin__user_slug__in=mentor_slugs).order_by('id')
    
    return render(request, 'administration/student/new_search_all.html',
                  {'students': students,
                   'students_pi':students_pi,
                   'mentors':mentors,
                   'mentors_pi':mentors_pi,
                   })




@student_future_student_parent_admin_user_required
def new_search_alumni(request):
    # Check Sessions
    print(f"--------------------Session Check New-Search-Alumni-----------------------")
    for key, value in request.session.items():
        print(f"Session-Key: {key} => Session-values: {value}")
    print(f"--------------------Session Analysis-----------------------")

    # Check Current Student Profile is completed or not ?
    if request.user.user_type == 3:
        student_obj = Student.objects.get(
            admin__slug=request.user.slug)

        app = Application.objects.get(admin=request.user)
        basic_info = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id,
                                                                                       user_slug=request.user.slug)
        
        print("-----------------New Search Alumni-----------------")
        print("Basic Info Object - ", basic_info)
        # if basic_info.about_me is None:
        #     return redirect('administration:student_profile_step_1')
    
    # Parents
    if request.user.user_type == 5:
        student_obj = Parent.objects.get(
            admin__slug=request.user.slug)
        print("Parent registering Student - ", student_obj)
    
    # Future Student
    if request.user.user_type == 12:
        student_obj = FutureStudent.objects.get(
            admin__slug=request.user.slug)
        print("Future Student - ", student_obj)

    
    reported_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                               is_removed=False).values_list('reported_user')
    # Exclude users from which current user get reported from
    reported_by_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                  is_removed=False).values_list('report_by_user')
    
    # List of Mentors
    mentors = Mentor.objects.filter(
        admin__is_active=True,profile_status=True,
        school=SCHOOL_OBJECT).exclude(Q(admin__id__in=reported_users) | Q(admin__id__in=reported_by_users), )
    temp =[]
    for i in mentors:
        if i.admin.slug and i.admin.slug not in temp:
            temp.append(i.admin.slug)
    
    # Get Filters for Mentor object from personal_information database.
    queryset = MentorPersonalInformation.objects.using(
        'afm_personal_information').filter(admin__user_slug__in=temp).order_by('id')
    filtered_qs = MentorPersonalFilter(request.GET, queryset)
    paginated_filtered = Paginator(filtered_qs.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)
        
    context = {
        'mentors': mentors, 
        'personal_info_list': page_obj, 
        'form': filtered_qs.form,
        'page_obj': page_obj, 
        'student': student_obj,
        }

    context['signupform'] = FutureStudentSignupForm()
    if request.method == "POST":
        chat_slug = request.POST.get('chat_slug')
        print("Session Chat Slug - ", chat_slug)
        futurestudent = FutureStudent.objects.get(admin=request.user)
        signupform = FutureStudentSignupForm(request.POST, instance = futurestudent)
        if signupform.is_valid():
            futurestudent = signupform.save(commit=False)
            futurestudent.save()
            print("----------------Future Student Created-----------------")
            print("Future Student Signup process finished........")
            print("Future Student - ", futurestudent.admin.username)
            print("Deleting session......")
            return redirect("administration:new_search_alumni")
            # return redirect("messaging:comment_mentor_public_profile_twfl", chat_slug)

    print("Context - ", context)
    return render(request, 'administration/student/new_search_mentors.html',context)



def new_search_students(request):
    print("----------------------------Session-----------------------------")
    for key,value in request.session.items():
        print(f"Key : {key}")
        print(f"Value: {value}")
    reported_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                               is_removed=False).values_list('reported_user')
    # Exclude users from which current user get reported from
    reported_by_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                  is_removed=False).values_list('report_by_user')
    students = Student.objects.filter(
        admin__is_active=True,profile_status=True,school=SCHOOL_OBJECT
        ).exclude(Q(admin__id__in=reported_users) | Q(admin__id__in=reported_by_users))
    temp = []
    for i in students:
        if i.admin.slug and i.admin.slug not in temp:
            temp.append(i.admin.slug)
    print("temp - ", temp)
    # Get Filters for Mentor object from personal_information database.
    queryset = StudentPersonalInformation.objects.using(
        'afm_personal_information').filter(admin__user_slug__in=temp).order_by('id')
    print("Student count - ", queryset.count())
    # Apply filter
    filtered_qs = StudentFilter(request.GET, queryset)
    # Apply Pagination
    paginated_filtered = Paginator(filtered_qs.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    return render(request, 'administration/student/new_search_students.html',
                  {'students': students,
                   'personal_info_list': page_obj,
                   'form': filtered_qs.form,
                   'page_obj': page_obj})




@future_student_special_mentor_user_required
def search_students_twfl(request):
    reported_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                               is_removed=False).values_list('reported_user')
    # Exclude users from which current user get reported from
    reported_by_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                  is_removed=False).values_list('report_by_user')
    students = Student.objects.filter(
        admin__is_active=True,
        school=SCHOOL_OBJECT).exclude(Q(admin__id__in=reported_users) | Q(admin__id__in=reported_by_users)).exclude(
        currently_studying_course=None, )
    temp = []
    for i in students:
        if i.admin.slug and i.admin.slug not in temp:
            temp.append(i.admin.slug)
    # Get Mentors object of personal_information database with currently_studying as Medicine
    queryset = AppBasicInformation.objects.using(
        'afm_personal_information').filter(user_slug__in=temp).order_by('id')
    # Apply filter
    filtered_qs = StudentSearchFilter(request.GET, queryset)
    # Apply Pagination
    paginated_filtered = Paginator(filtered_qs.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    return render(request, 'administration/student/search_students.html',
                  {'students': students,
                   'personal_info_list': page_obj,
                   'form': filtered_qs.form,
                   'page_obj': page_obj})



def ajax_loggeduser_status(request,slug):
    loggeduser = CustomUser.objects.get(slug=slug)
    status = loggeduser.loggeduser.online_status
    print("-------------------------AJAX Loggeduser Status---------------------------")
    print("Slug - ", slug)
    print("Status - ", loggeduser.loggeduser.online_status)
    return JsonResponse({"slug":slug, "onlinestatus":status})



def student_profile_step_1(request):
    custom_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    student_instance = StudentPersonalInformation.objects.using(
        'afm_personal_information').get(admin=custom_user)
    basic_info = AppBasicInformation.objects.using('afm_personal_information').get(user_slug=request.user.slug)
    student_form = StudentPersonalInformationFirstStepForm(instance=student_instance)
    custom_form = CustomUserPersonalInformationForm(instance=custom_user)

    # print("Custom Form - ", custom_form)
    # print("Student Form - ", student_form)

    if request.method == 'POST':
        custom_form = CustomUserPersonalInformationForm(
            request.POST, instance=custom_user)
        student_form = StudentPersonalInformationFirstStepForm(
            request.POST, instance=student_instance)

        if student_form.is_valid() and custom_form.is_valid():
            custom_object = custom_form.save()
            student = student_form.save(commit=False)
            student.about_me = custom_object.about_me
            basic_info.about_me = custom_object.about_me
            basic_info.save()
            student.save()
            print("Custom object about me - ", custom_object.about_me)
            print("Student object about me - ", student.about_me)
            print("Basic Info object about me - ", basic_info.about_me)
            
            return redirect("administration:student_profile_step_2")
        else:
            print(student_form.errors)
            print(custom_form.errors)
            messages.error(request, "Invalid form, Please enter valid details")
    return render(request, 'administration/student/student_profile_step_1.html',
                  {'form': student_form, 'form2': custom_form, 'student_instance': student_instance})



def student_profile_step_2(request):
    custom_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    student_instance = StudentPersonalInformation.objects.using(
        'afm_personal_information').get(admin=custom_user)
    
    form = ProfilePhotoForm(instance=custom_user)
    consent_form = StudentConsentForm(instance=student_instance)
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=custom_user)
        consent_form = StudentConsentForm(request.POST, instance=student_instance)
        if form.is_valid() and consent_form.is_valid():
            form.save()
            consent_form.save()
            return redirect("administration:dashboard")
        else:
            messages.error(request, "Invalid form, Please enter valid details")
    return render(request, 'administration/student/student_profile_photo.html',
                  {'form': form, 'mentor_pi': student_instance, 'consent_form': consent_form})



def student_profile(request,slug):
    student_info = Student.objects.get(admin__slug=slug)
    student_personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=slug)
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=slug)
    
    return render(request, 'administration/student/student_profile.html',
                {'student_info': student_info, 'student_personal_info': student_personal_info,
                'pi_user':pi_user})



# -------------------------------------------------------------
# MENTOR MODULES
# -------------------------------------------------------------


'''
Function   : get_template
Description: Mentor public profile page
Parameters : user_mentor_pi, user_mentor
Return     : Mentor user public profile page
'''


def get_template(request, user_mentor_pi, user_mentor):
    # Check if mentor is not from dentistry or medicine
    # if not user_mentor.profile_status or user_mentor_pi.currently_studying != 6:
    #     return redirect('administration:page_not_found')
    # Get mentor feedbacks
    testimonials = MentorFeedback.objects.filter(status=True, mentor=user_mentor)
    # Get mentor posts
    queryset = Post.objects.filter(post_status=2, author=user_mentor)
    # Pagination
    # paginated_filtered = Paginator(queryset, 1)
    # page_number = request.GET.get('page')
    # page_obj = paginated_filtered.get_page(page_number)
    mentor_message_form = MessageMentorForm()
    mentorbookingleads_form = MentorBookingLeadsForm()

    if request.method == "POST":
        mentor_message_form = MessageMentorForm(request.POST)
        if mentor_message_form.is_valid():
            instance = mentor_message_form.save(commit=False)
            instance.admin = user_mentor.admin
            instance.save()
            sent_mail = message_mentor_twfl(request, instance)
            messages.success(
                request, "We received your request, we will get back to you shortly.")
        else:
            print(mentor_message_form.errors)
            messages.error(request, "Invalid Form")
    return render(request, "administration/mentor/student_single_mentor.html",
                  {'mentor': user_mentor, 'user_mentor_pi': user_mentor_pi, 'mentor_posts': queryset,
                   'mentorbookingleads_form': mentorbookingleads_form,
                   'testimonials': testimonials,
                   'mentor_message_form': mentor_message_form, })


'''
Function   : student_single_mentor_twfl
Description: Mentor public profile page using mentor personal information
Parameters : name_slug, currently_studying_slug, institute_in, country_slug, slug
Return     : Mentor user public profile page
'''


def student_single_mentor_twfl(request, name_slug, currently_studying_slug, institute_in, country_slug):
    # Get mentor object from db2(Database for personal information)
    user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug, admin__country_slug=country_slug,
        url_slug=None)
    temp = []
    # Get list of available user slugs
    for i in user_mentor_pi:
        temp.append(i.admin.user_slug)

    if Mentor.objects.filter(admin__slug__in=temp, institute__institute_slug=institute_in,
                             profile_status=True).exists():
        # Get mentor object from db1(Database for general information)
        user_mentor = Mentor.objects.get(admin__slug__in=temp, institute__institute_slug=institute_in,
                                         profile_status=True, school=SCHOOL_OBJECT)
    else:
        # Get mentor object from db1(Database for general information)
        user_mentor = Mentor.objects.get(admin__slug__in=temp, institute_name_slug=institute_in, profile_status=True,
                                         school=SCHOOL_OBJECT)
        # user_mentor = Mentor.objects.get(admin__slug=user_mentor_pi.admin.user_slug)

    user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=user_mentor.admin.slug,
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug, admin__country_slug=country_slug,
        url_slug=None)
    return get_template(request, user_mentor_pi, user_mentor)


'''
Function   : student_single_mentor_twfl
Description: Mentor public profile page using mentor personal information
Parameters : name_slug, currently_studying_slug, institute_in, country_slug, slug
Return     : Mentor user public profile page
'''


def student_single_mentor_using_url_slug_twfl(request, name_slug, currently_studying_slug, institute_in, country_slug,
                                              url_slug):
    # Get mentor object from db2(Database for personal information)
    user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug, admin__country_slug=country_slug,
        url_slug=url_slug)
    temp = []
    # Get list of available user slugs
    for i in user_mentor_pi:
        temp.append(i.admin.user_slug)
    if Mentor.objects.filter(admin__slug__in=temp, institute__institute_slug=institute_in,
                             profile_status=True).exists():
        # Get mentor object from db1(Database for general information)
        user_mentor = Mentor.objects.get(admin__slug__in=temp, institute__institute_slug=institute_in,
                                         profile_status=True, school=SCHOOL_OBJECT)
    else:
        # Get mentor object from db1(Database for general information)
        user_mentor = Mentor.objects.get(admin__slug__in=temp, institute_name_slug=institute_in, profile_status=True,
                                         school=SCHOOL_OBJECT)
        # user_mentor = Mentor.objects.get(admin__slug=user_mentor_pi.admin.user_slug)

    user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=user_mentor.admin.slug,
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug, admin__country_slug=country_slug,
        url_slug=url_slug)
    return get_template(request, user_mentor_pi, user_mentor)


'''
Function   : student_single_mentor_using_slug_twfl
Description: Mentor public profile page using mentor slug. In any case if two mentors has same name_slug, 
             currently_studying_slug, institute_in, and country_slug then we will use another unique parameter 
             'slug' as argument. 
Parameters : name_slug, currently_studying_slug, institute_in, country_slug, slug
Return     : Mentor user public profile page
'''


def student_single_mentor_using_slug_twfl(request, name_slug, currently_studying_slug, institute_in, country_slug,
                                          slug):
    user_mentor = Mentor.objects.get(admin__slug=slug, school=SCHOOL_OBJECT)
    user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=user_mentor.admin.slug)
    return get_template(request, user_mentor_pi, user_mentor)



def alumni_public_profile1(request,currently_studying_slug,name_slug,country_slug):
    # Get mentor object from db2(Database for personal information)
    user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug, admin__country_slug=country_slug,
        url_slug=None)
    temp = []
    # Get list of available user slugs
    for i in user_mentor_pi:
        temp.append(i.admin.user_slug)

    if Mentor.objects.filter(admin__slug__in=temp,
                             profile_status=True).exists():
        # Get mentor object from db1(Database for general information)
        user_mentor = Mentor.objects.get(admin__slug__in=temp, 
                                         profile_status=True, school=SCHOOL_OBJECT)
    else:
        # Get mentor object from db1(Database for general information)
        user_mentor = Mentor.objects.get(admin__slug__in=temp, profile_status=True,
                                         school=SCHOOL_OBJECT)
        # user_mentor = Mentor.objects.get(admin__slug=user_mentor_pi.admin.user_slug)

    user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=user_mentor.admin.slug,
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug, admin__country_slug=country_slug,
        url_slug=None)
    return get_template(request, user_mentor_pi, user_mentor)



def alumni_public_profile(request,currently_studying_slug,name_slug,country_slug):
    mentors_from_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug, admin__country_slug=country_slug,
        url_slug=None)
    temp = []
    # Get list of available user slugs
    for i in mentors_from_pi:
        temp.append(i.admin.user_slug)
    print("slugs in temp - ", temp)
    mentor = Mentor.objects.get(admin__slug__in=temp, profile_status=True,school=SCHOOL_OBJECT)

    mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=mentor.admin.slug,
        admin__name_slug=name_slug, currently_studying_slug=currently_studying_slug, admin__country_slug=country_slug,
        url_slug=None)
    print("Mentor Institute - ", mentor.institute, mentor.institute_name,mentor.institute_name_slug)
    chat_signup_form = ChatRegistrationForm()

    if request.method == "POST":
        chat_signup_form = ChatRegistrationForm(request.POST)
        if chat_signup_form.is_valid():
            print("chat signup form valid....")
            chat_user = chat_signup_form.save(commit=False)
            chat_user.user_type = 12
            chat_user.is_active = True
            chat_user.save()
            print("Manual Chat Signup based Registration successful - ",chat_user.id, chat_user )
            print("Future Student created: ", chat_user.id, chat_user.slug, chat_user.email)
            print("Triggered create_user_profile signal successfully.")        
            print("----------------------Signal successful------------------------")
            
            login(request, chat_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("administration:new_search_alumni")
        else:
            print(chat_signup_form.errors)

    context = {
            'mentor':mentor,
            'mentor_pi':mentor_pi,
            'form':chat_signup_form
        }

    return render(request, "administration/mentor/alumni_public_profile.html", context)




def ifg_student_public_profile(request,user_slug):
    
    print("slug - ", user_slug)
    student_pi = StudentPersonalInformation.objects.using('afm_personal_information').get(
    admin__user_slug=user_slug)

    print("Student Personal slug - ", student_pi.admin.user_slug)
    student = Student.objects.get(admin__slug=student_pi.admin.user_slug)
    print("Student - ", student)
    print("----------------------Student Public Profile view triggered--------------------")


    chat_signup_form = ChatRegistrationForm()

    if request.method == "POST":
        chat_signup_form = ChatRegistrationForm(request.POST)
        if chat_signup_form.is_valid():
            print("chat signup form valid....")
            chat_user = chat_signup_form.save(commit=False)
            chat_user.user_type = 12
            chat_user.is_active = True
            chat_user.save()
            print("Manual Chat Signup based Registration successful - ",chat_user.id, chat_user )
            print("Future Student created: ", chat_user.id, chat_user.slug, chat_user.email)
            print("Triggered create_user_profile signal successfully.")        
            print("----------------------Signal successful------------------------")
            
            login(request, chat_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("administration:new_search_alumni")
        else:
            print(chat_signup_form.errors)

    context = {
        'student':student,
        'student_pi':student_pi,
        'form':chat_signup_form
    }

    return render(request, "administration/student/student_public_profile.html", context)
   

'''
Function   : message_mentor_twfl
Description: Sent email to tag for new lead
Parameters : MessageMentorForm instance
Return     : Mentor user public profile page
'''

def message_mentor_twfl(request, instance):
    html_message = loader.render_to_string('administration/email/contact_mail.html',
                                           {
                                               'contact': instance,
                                               'title': 'New Message Lead from',
                                           })
    try:
        mail = send_mail('New Message for Mentor', "Hello", None, [mail_send_from],
                         html_message=html_message)
        message = "success"
    except SMTPException as e:
        print(f'error  : {e}')
        message = e
    else:
        message = "Mail could not be sent, Please contact administrator"
    return message


'''
Class         : MentorBookingLeadsList 
Parameters    : --
Return        : List of Mentor booking leads with pagination
Authorisation : Admin
'''


class MentorBookingLeadsList(ListView):
    model = MentorBookingLeads

    def get_context_data(self, **kwargs):
        context = super(MentorBookingLeadsList, self).get_context_data(**kwargs)
        filtered_qs = MentorBookingLeadsFilter(self.request.GET,
                                               queryset=MentorBookingLeads.objects.all().order_by('-created_at'))
        context['filter'] = filtered_qs
        paginated_filter = Paginator(filtered_qs.qs, 10)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginated_filter.get_page(page_number)
        return context


'''
Class          : mentor_booking_leads 
Parameters     : slug(Mentor unique id)
Return/Results : Submit booking lead and send email notification to admin and to email submitted in form 
Authorisation  : Guest user
'''


def mentor_booking_leads(request, slug):
    user_obj = Mentor.objects.get(admin__slug=slug)
    form = MentorBookingLeadsForm(request.POST or None)
    return_path = '/'
    if request.method == 'POST' and form.is_valid():
        # Get path of the page the request is come from so will redirect it to the same page once the form is submitted
        # successfully
        return_path = request.POST['return_path']
        obj = form.save(commit=False)
        obj.mentor = user_obj
        obj.save()
        mail_obj = MentorBookingLeads.objects.get(id=obj.id)
        subject = "New Mentor Booking Lead"
        html_message = loader.render_to_string('email/mentor_booking_leads.html', {'mail_obj': mail_obj, })
        try:
            # Send email
            mail = send_mail(subject, "Hello", None, [mail_send_from, mail_obj.email],
                             html_message=html_message)
        except:
            print("Fail")
        messages.success(request, "Thank you for your response, We will get back to you soon.")
        return redirect(return_path)
    link = getmentorprofileurl(slug)
    messages.error(request, "Invalid form, Please enter valid details")
    return redirect(link)



#------------------------------------Alumni Profile--------------------------------------#



'''
Function   : Update Profile Step 1
Description: Upload public profile information
Parameters : --
Return     : Update Profile Step 2
'''


@mentor_user_required
def upload_public_information_twfl(request):
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    mentor_pi_instance = MentorPersonalInformation.objects.using(
        'afm_personal_information').get(admin=pi_user)
    # if mentor_pi_instance.consent4:
    #     return redirect('administration:dashboard')
    user_pi_form = MentorUpdateInformationFirstStepForm(instance=mentor_pi_instance)
    custom_user_pi_form = CustomUserPersonalInformationForm(instance=pi_user)
    if request.method == 'POST':
        custom_user_pi_form = CustomUserPersonalInformationForm(
            request.POST, request.FILES, instance=pi_user)
        user_pi_form = MentorUpdateInformationFirstStepForm(
            request.POST, request.FILES, instance=mentor_pi_instance)

        if user_pi_form.is_valid() and custom_user_pi_form.is_valid():
            # try:
            post = user_pi_form.save(commit=False)
            post.save(using="afm_personal_information")
            user_pi_form.save_m2m()
            custom_user_pi_form.save()
            # user_form.save()
            print("Step 1: forms saved and transferred to Step 2.........")
            return redirect("administration:upload_private_information_twfl")
        else:
            print(user_pi_form.errors)
            print(custom_user_pi_form.errors)
            # print(user_form.errors)
            messages.error(request, "Invalid form, Please enter valid details")
    return render(request, 'administration/mentor/upload_public_information.html',
                  {'form': user_pi_form, 'form2': custom_user_pi_form, 'mentor_pi': mentor_pi_instance})


'''
Function   : Update Profile Step 2
Description: Upload private information
Parameters : --
Return     : Update Profile Step 3
'''


@mentor_user_required
def upload_private_information_twfl(request):
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    mentor_pi_instance = MentorPersonalInformation.objects.using(
        'afm_personal_information').get(admin=pi_user)

    # if mentor_pi_instance.consent4:
    #     return redirect('administration:dashboard')

    # Check if public information form is field before coming on this stage
    # if pi_user.phone is None:
    #     return redirect('administration:upload_public_information_twfl')
    
    user_form = MentorProfileForm(
        instance=Mentor.objects.get(admin=request.user))
    user_pi_form = MentorUpdateInformationSecondStepForm(instance=mentor_pi_instance)
    if request.method == 'POST':
        user_pi_form = MentorUpdateInformationSecondStepForm(
            request.POST, request.FILES, instance=mentor_pi_instance)
        user_form = MentorProfileForm(
            request.POST, request.FILES, instance=Mentor.objects.get(admin=request.user))
        if user_pi_form.is_valid() and user_form.is_valid():
            # try:
            post = user_pi_form.save(commit=False)
            post.save(using="afm_personal_information")
            user_pi_form.save_m2m()
            obj = user_form.save(commit=False)
            obj.institute_name = user_form.cleaned_data['institute_name']
            if user_form.cleaned_data['institute_list'] not in ['Other', '']:
                obj.institute_name = user_form.cleaned_data['institute_list']
            obj.save()
            print("Step 2: Questions saved successfully.....")
            return redirect("administration:upload_profile_photo_and_consent_twfl")
        else:
            print(user_pi_form.errors)
            print(user_form.errors)
            messages.error(request, "Invalid form, Please enter valid details")
    return render(request, 'administration/mentor/upload_private_information.html',
                  {'form': user_pi_form, 'form3': user_form, 'mentor_pi': mentor_pi_instance,
                   'mentor': Mentor.objects.get(admin=request.user)})


'''
Function   : Update Profile Step 3
Description: Upload profile photo on Step 3 of update form
Parameters : --
Return     : Dashboard
'''


@mentor_user_required
def upload_profile_photo_and_consent_twfl(request):
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    mentor_pi_instance = MentorPersonalInformation.objects.using(
        'afm_personal_information').get(admin=pi_user)
    # if mentor_pi_instance.consent4:
    #     return redirect('administration:dashboard')
    form = ProfilePhotoForm(instance=pi_user)
    consent_form = MentorConsentForm(instance=mentor_pi_instance)
    if request.method == 'POST':
        form = ProfilePhotoForm(
            request.POST, request.FILES, instance=pi_user)
        consent_form = MentorConsentForm(
            request.POST, instance=mentor_pi_instance)
        if form.is_valid() and consent_form.is_valid():
            form.save()
            consent_form.save()
            return redirect("administration:dashboard")
        else:
            messages.error(request, "Invalid form, Please enter valid details")
    return render(request, 'administration/mentor/upload_profile_photo.html',
                  {'form': form, 'mentor_pi': mentor_pi_instance, 'consent_form': consent_form})



#------------------------------------Current Student Profile--------------------------------------#


def current_student_profile_step_1(request):
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    student_pi_instance = StudentPersonalInformation.objects.using(
        'afm_personal_information').get(admin=pi_user)
   
    custom_user_pi_form = CustomUserPersonalInformationForm(instance=pi_user)
    student_step1_form = StudentProfileStep1Form(instance=student_pi_instance)
    
    if request.method == 'POST':
        custom_user_pi_form = CustomUserPersonalInformationForm(
            request.POST, request.FILES, instance=pi_user)
        student_step1_form = StudentProfileStep1Form(
            request.POST, request.FILES, instance=student_pi_instance)

        if student_step1_form.is_valid() and custom_user_pi_form.is_valid():
            custom_user_pi_form.save()
            student_personal_information = student_step1_form.save(commit=False)
            student_personal_information.save(using="afm_personal_information")
            print("Step 1: forms saved and transferred to Step 2.........")
            return redirect("administration:current_student_profile_step_2")
        else:
            print(student_step1_form.errors)
            print(custom_user_pi_form.errors)
            messages.error(request, "Invalid form, Please enter valid details")
            
    return render(request, 'administration/student/current_student_profile_step_1.html',
                  {'studentform': student_step1_form, 'customform': custom_user_pi_form, 'student': student_pi_instance})




def current_student_profile_step_2(request):
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    student_pi_instance = StudentPersonalInformation.objects.using(
        'afm_personal_information').get(admin=pi_user)

    questionform = StudentQuestionForm(instance=Student.objects.get(admin=request.user))
    
    if request.method == 'POST':
        questionform = StudentQuestionForm(request.POST, instance=Student.objects.get(admin=request.user))
        print("Whether Question Form is valid or not ? ", questionform.is_valid())
        if questionform.is_valid():
            question = questionform.save(commit=False)
            question.save(using="afm")
            print("Step 2: Questions saved successfully.....")
            return redirect("administration:current_student_profile_step_3")
        else:
            print("Not valid ........")
            print(questionform.errors)
            # messages.error(request, "Invalid form, Please enter valid details")
            return redirect("administration:current_student_profile_step_3")
    return render(request, 'administration/student/current_student_profile_step_2.html',
                  {'form': questionform, 'student': student_pi_instance})




def current_student_profile_step_3(request):
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=request.user.slug)
    student_pi_instance = StudentPersonalInformation.objects.using(
        'afm_personal_information').get(admin=pi_user)
    # if student_pi_instance.consent1:
    #     return redirect('administration:dashboard')
    form = ProfilePhotoForm(instance=pi_user)
    consent_form = StudentConsentForm(instance=student_pi_instance)
    
    if request.method == 'POST':
        form = ProfilePhotoForm(request.POST, request.FILES, instance=pi_user)
        consent_form = StudentConsentForm(request.POST, instance=student_pi_instance)
        if form.is_valid() and consent_form.is_valid():
            form.save()
            consent_form.save()
            print("Step 3: Profile Photo saved.....")
            return redirect("administration:thanking")
        else:
            messages.error(request, "Invalid form, Please enter valid details")
    return render(request, 'administration/student/current_student_profile_step_3.html',
                  {'form': form, 'consent_form': consent_form, 'student': student_pi_instance})



def thanking(request):
    return render(request, 'administration/thanking.html')




# ----------------------------------------------------------------------------
#     INSTITUTE MODULE
# ----------------------------------------------------------------------------

'''
Date       : 12/17/2020 
Function   : institute_admin_registration_twfl
Description: Create Institute Admin user for Institutes
Parameters : --
Return     : Creat Institute Admin User
'''


@institute_user_required
def institute_admin_registration_twfl(request):
    institute_instance = Institute.objects.get(admin=request.user)
    institute_admins = InstituteAdmin.objects.filter(
        institute=institute_instance)
    if request.method != "POST":
        form = InstituteAdminRegistrationForm
        return render(request, 'registration/institute_registration.html',
                      {'form': form, 'institute_admins': institute_admins})
    else:
        user_form = InstituteAdminRegistrationForm(request.POST)
        if user_form.is_valid():
            # try:
            institute_admin = user_form.save(commit=False)
            # Select user type as Institute Admin
            institute_admin.user_type = 6
            institute_admin.save()
            # Get InstituteAdmin model object for this user
            institute_admin_user = InstituteAdmin.objects.get(
                admin=institute_admin)
            # Assign this institute admin to current user(Institute user)
            institute_user = Institute.objects.get(admin=request.user)
            institute_admin_user.institute = institute_user
            institute_admin_user.save()
            messages.success(request, "Successfully Registered")
            return HttpResponseRedirect(reverse("administration:institute_admin_registration_twfl"))
        else:
            print(user_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
            return render(request, "registration/institute_registration.html",
                          {'form': user_form, 'institute_admins': institute_admins})


'''
Date       : 12/17/2020 
Function   : institute_mentors_twfl
Description: Get list of mentors of current institute
Parameters : --
Return     : List of mentors
'''


@institute_user_required
def institute_mentors_twfl(request):
    institute_instance = Institute.objects.get(admin=request.user)
    # Get mentors of current user institute
    mentors_list = Mentor.objects.filter(
        institute=institute_instance, profile_status=True)
    temp = []
    for i in mentors_list:
        temp.append(i.admin.slug)
    # Get mentors personal information objects
    pi_info = MentorPersonalInformation.objects.using('afm_personal_information').filter(admin__user_slug__in=temp)
    return render(request, 'administration/institute/list_mentors.html',
                  {'mentors': mentors_list, 'personal_info_list': pi_info})


'''
Function   : how_it_work_twfl
Description: Get How it works page
Parameters : --
Return     : Redirects to How it works page
'''


@login_required
def how_it_work_twfl(request):
    # If current user is Institute/university
    if request.user.user_type == 2:
        return render(request, "administration/university-how-it-work.html")
    return render(request, "administration/how_it_work.html")


'''
Function   : tech_support_twfl
Description: Send email notification for tech support request
Parameters : --
Return     : Send email
'''


@login_required
def tech_support_twfl(request):
    form = TechSupportForm()
    faq_list = Faq.objects.filter(user_type__in=[4, 0], status='publish').order_by('rank')
    if request.method == 'POST':
        form = TechSupportForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            send_email_notification.delay('Tech Support Request',
                                    'administration/email/tech_support_mail.html',
                                    [mail_send_from],
                                    {
                                        'user_type': request.user.user_type,
                                        'first_name': request.user.first_name,
                                        'slug': request.user.slug,
                                        'message': instance.message,
                                        'subject': instance.subject,
                                    }
                                    )
            messages.success(
                request, "We received your request, we will get back to you shortly.")
        else:
            messages.error(request, "Invalid Data")
        return redirect('administration:tech_support_twfl')
    return render(request, 'administration/tech_support.html', {'form': form, 'faq_list': faq_list})


# ----------------------------------------------------------------------------
#     ADMIN MODULE
# ----------------------------------------------------------------------------

'''
Function   : view_applications_of_user_twfl
Description: View user applications or
Parameters : --
Return     : Send email
'''


@school_admin_user_required
def view_applications_of_user_twfl(request, user_slug):
    # Application status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    queryset = Application.objects.filter(
        admin__slug=user_slug, status__in=[0, 1, 2, 3])
    user = CustomUser.objects.get(slug=user_slug)
    return render(request, "administration/parent/parent_applications.html",
                  {'list_applications': queryset, 'user': user})


'''
Function   : list_students_twfl
Description: List registered students with personal information
Parameters : --
Return     : redirect to list student page
'''


@school_admin_user_required
def list_students_twfl(request):
    # Get all students form Database1
    students = Student.objects.filter(school=SCHOOL_OBJECT).exclude(admin=None)
    temp = []
    for i in students:
        temp.append(i.admin.slug)
    # Get students personal information objects(Database2)
    queryset = StudentPersonalInformation.objects.using(
        'afm_personal_information').filter(admin__user_slug__in=temp).order_by(
        '-created_at')
    # Apply filter
    filtered_qs = StudentFilter(request.GET, queryset)
    paginated_filtered = Paginator(filtered_qs.qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)
    #  return render(request, "administration/admin/my_students.html",
    return render(request, "administration/admin/list_students.html",
                  {'students': students, 'personal_info_list': page_obj, 'form': filtered_qs.form,
                   'page_obj': page_obj})


'''
Function   : list_parents_twfl
Description: List registered parents
Parameters : --
Return     : redirect to list parent page
'''


@school_admin_user_required
def list_parents_twfl(request):
    if request.method != 'POST':
        # Get all parents form Database1
        queryset = Parent.objects.exclude(admin=None).order_by('-admin__created_at')
        queryset = ParentFilter(request.GET, queryset)
        paginated_filtered = Paginator(queryset.qs, 100)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)
        return render(request, "administration/admin/list_parents.html",
                      {'queryset': page_obj, 'title': 'Parent', 'page_obj': page_obj, 'form': queryset.form, })
    else:
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(CustomUser, id=admin_id)
        # Deactivate user
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
    return redirect('administration:list_parents_twfl')


'''
Function   : system_mentor_registration_twfl
Description: Register system mentor
Parameters : --
Return     : System Mentor register page
'''


@super_admin_user_required
def system_mentor_registration_twfl(request):
    if request.method != "POST":
        form = SystemMentorRegistrationForm
        return render(request, 'registration/registration_form.html',
                      {'form': form, 'title': 'System Mentor Registration'})
    else:
        user_form = SystemMentorRegistrationForm(request.POST)
        if user_form.is_valid():
            # try:
            app_admin = user_form.save(commit=False)
            # System mentor user type is 9
            app_admin.user_type = 9
            app_admin.save()
            messages.success(request, "Successfully Registered")
            return redirect('administration:list_system_mentors_twfl')
        else:
            print(user_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "registration/registration_form.html",
                  {'form': user_form, 'title': 'System Mentor Registration'})


'''
Function   : system_recruiter_registration_twfl
Description: Register system recruiter
Parameters : --
Return     : System recruiter register page
'''


@super_admin_user_required
def system_recruiter_registration_twfl(request):
    if request.method != "POST":
        form = SystemRecruiterRegistrationForm
        return render(request, 'registration/registration_form.html',
                      {'form': form, 'title': 'System Recruiter Registration'})
    else:
        user_form = SystemRecruiterRegistrationForm(request.POST)
        if user_form.is_valid():
            # try:
            app_admin = user_form.save(commit=False)
            # System recruiter user type is 10
            app_admin.user_type = 10
            app_admin.save()
            messages.success(request, "Successfully Registered")
            return redirect('administration:list_system_recruiter_twfl')
        else:
            print(user_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "registration/registration_form.html",
                  {'form': user_form, 'title': 'System Recruiter Registration'})


'''
Function   : recruiter_registration_twfl
Description: Register recruiter
Parameters : --
Return     : recruiter register page
'''


@super_admin_user_required
def recruiter_registration_twfl(request):
    if request.method != "POST":
        form = RecruiterRegistrationForm
        return render(request, 'registration/registration_form.html',
                      {'form': form, 'title': 'Recruiter Registration'})
    else:
        user_form = RecruiterRegistrationForm(request.POST)
        if user_form.is_valid():
            # try:
            recruiter_form = user_form.save(commit=False)
            # System recruiter user type is 8
            recruiter_form.user_type = 8
            recruiter_form.save()
            # Get recruiter objects which will get created with post_save signal
            recruiter = Recruiter.objects.get(admin=recruiter_form)
            recruiter.work_type = user_form.cleaned_data['work_type']
            recruiter.save()
            messages.success(request, "Successfully Registered")
            return redirect('administration:list_recruiters_twfl')
        else:
            print(user_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "registration/registration_form.html",
                  {'form': user_form, 'title': 'Recruiter Registration'})


@super_admin_user_required
def school_registration_twfl(request):
    if request.method != "POST":
        form = SchoolRegistrationForm
        return render(request, 'registration/registration_form.html',
                      {'form': form, 'title': 'School Registration'})
    else:
        user_form = SchoolRegistrationForm(request.POST)
        if user_form.is_valid():
            # try:
            recruiter_form = user_form.save(commit=False)
            # System recruiter user type is 8
            recruiter_form.user_type = 8
            recruiter_form.save()
            # Get recruiter objects which will get created with post_save signal
            recruiter = Recruiter.objects.get(admin=recruiter_form)
            recruiter.school_name = user_form.cleaned_data['school_name']
            recruiter.website = user_form.cleaned_data['website']
            recruiter.save()
            messages.success(request, "Successfully Registered")
            return redirect('administration:list_recruiters_twfl')
        else:
            print(user_form.errors)
            messages.error(request, "Failed to register, Form is not valid")
    return render(request, "registration/registration_form.html",
                  {'form': user_form, 'title': 'Recruiter Registration'})


'''
Date       : 12/16/2020 
Function   : list_mentors_twfl
Description: List all the mentors available
Parameters : --
Return     : List Mentor page
'''


@school_admin_user_required
# @super_admin_user_required
def list_mentors_twfl(request):
    if request.method != 'POST':
        # Get all mentors from Database1
        mentors = Mentor.objects.exclude(admin=None).order_by('profile_status')
        # temp = []
        # for i in mentors:
        #     if MentorPersonalInformation.objects.using('afm_personal_information').filter(admin__user_slug=i.admin.slug).exists():
        #         temp.append(i.admin.slug)
        # print(temp)
        # Get all mentors personal information from Database1
        # queryset = MentorPersonalInformation.objects.using('afm_personal_information').filter(admin__user_slug__in = temp)
        queryset = MentorPersonalInformation.objects.using('afm_personal_information').all().order_by('-created_at')

        # from django.db.models import Case, When
        #
        # preserved = Case(*[When(admin__user_slug=pk, then=pos) for pos, pk in enumerate(temp)])
        # queryset = MentorPersonalInformation.objects.filter(admin__user_slug__in=temp).order_by(preserved)

        filtered_qs = MentorFilter(request.GET, queryset)
        # Get list of emails
        temp = []
        for slug in filtered_qs.qs.values_list('admin__user_slug'):
            temp.append(slug[0])
        temp2 = []
        for email in CustomUser.objects.filter(slug__in=temp).values_list('email'):
            temp2.append(email[0])
        # End Get list of emails
        paginated_filtered = Paginator(filtered_qs.qs, 50)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        return render(request, 'administration/admin/list_mentors.html',
                      {'mentors': mentors, 'personal_info_list': page_obj, 'form': filtered_qs.form,
                       'page_obj': page_obj, 'latepoint_form': LatepointLinkForm, 'list_user_emails': temp2})

    else:
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(CustomUser, id=admin_id)
        # Deactivate user
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('administration:list_mentors_twfl')


'''
Function   : list_system_mentors_twfl
Description: List all the mentors available
Parameters : --
Return     : List system mentor page
'''


@super_admin_user_required
def list_system_mentors_twfl(request):
    if request.method != 'POST':
        # Get all System mentors, System mentor user type is 9
        mentors = CustomUser.objects.filter(user_type=9)

        return render(request, 'administration/admin/list_system_mentors.html',
                      {'mentors': mentors, })

    else:
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(CustomUser, id=admin_id)
        # Deactivate User
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('administration:list_system_mentors_twfl')


@super_admin_user_required
def list_system_recruiter_twfl(request):
    if request.method != 'POST':
        recruiters = CustomUser.objects.filter(user_type=10)

        return render(request, 'administration/admin/list_system_recruiter.html',
                      {'recruiters': recruiters, })
    else:
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(CustomUser, id=admin_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('administration:list_system_recruiter_twfl')


@super_admin_user_required
def list_app_admin_twfl(request):
    if request.method != 'POST':
        app_admins = AppAdmin.objects.all()
        return render(request, 'administration/admin/list_app_admins.html',
                      {'app_admins': app_admins})
    else:
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(CustomUser, id=admin_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('administration:list_app_admin_twfl')


@super_admin_user_required
def list_institutes_twfl(request):
    if request.method != 'POST':
        institutes = Institute.objects.all()
        return render(request, 'administration/admin/list_institute.html',
                      {'institutes': institutes})
    else:
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(CustomUser, id=admin_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('administration:list_institutes_twfl')


@super_admin_user_required
def list_mentor_testimonials(request):
    queryset = MentorFeedback.objects.all()
    filtered_qs = TestimonialsFilter(request.GET, queryset)
    paginated_filtered = Paginator(filtered_qs.qs, 50)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)
    return render(request, 'administration/admin/list_testimonials.html',
                  {'list': page_obj, 'form': filtered_qs.form,
                   'page_obj': page_obj})


@super_admin_user_required
def list_recruiters_twfl(request):
    if request.method != 'POST':
        queryset = Recruiter.objects.all()
        filtered_qs = RecruiterFilter(request.GET, queryset)
        paginated_filtered = Paginator(filtered_qs.qs, 50)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)
        return render(request, "administration/admin/list_users.html",
                      {'queryset': page_obj, 'recruiter_search_form': filtered_qs.form,
                       'page_obj': page_obj, 'title': 'Recruiters'})

    else:
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(CustomUser, id=admin_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('administration:list_recruiters_twfl')


@super_admin_user_required
def list_future_students_twfl(request):
    if request.method != 'POST':
        queryset = FutureStudent.objects.exclude(admin=None).order_by('-created_at')
        filtered_qs = FutureStudentFilter(request.GET, queryset)
        paginated_filtered = Paginator(filtered_qs.qs, 50)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)
        return render(request, "administration/admin/list_future_students.html",
                      {'list': page_obj, 'form': filtered_qs.form,
                       'page_obj': page_obj, 'title': 'Future Students'})

    else:
        admin_id = request.POST.get('admin_id')
        user = get_object_or_404(CustomUser, id=admin_id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect('administration:list_future_students_twfl')


@super_admin_user_required
def list_lead_institute_twfl(request):
    list = InstituteLead.objects.all()
    return render(request, 'administration/admin/list_institute_leads.html',
                  {'list': list})


@super_admin_user_required
def list_tech_support_twfl(request):
    queryset = TechSupport.objects.all()
    queryset = TechSupportFilter(request.GET, queryset)
    paginated_filtered = Paginator(queryset.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    return render(request, 'administration/admin/tech_support_leads.html',
                  {'list': page_obj, 'form': queryset.form,
                   'page_obj': page_obj})


@super_admin_user_required
def list_contact_leads_twfl(request):
    queryset = ContactUs.objects.all()
    queryset = ContactUsFilter(request.GET, queryset)
    paginated_filtered = Paginator(queryset.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    return render(request, 'administration/admin/contact_leads.html',
                  {'list': page_obj, 'form': queryset.form,
                   'page_obj': page_obj})


@super_admin_user_required
def change_status_is_active_twfl(admin_id):
    user = get_object_or_404(CustomUser, id=admin_id)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return user


'''
Function   : greetings_message_twfl
Description: Default greeting messages 
Parameters : --
Return     : create object message objects
'''


def greetings_message_twfl(request, receiver):
    admin_profile = CustomUser.objects.filter(user_type=0).first()
    message = "Please use this page to send messages directly to the International Foundation Group Team with your questions, feedback " \
              "and anything of interest, we would love to hear from you!<br><br>" \
              "Please add signup@theapplygroup.com to your email contacts to avoid messages from potential " \
              "students/parents being blocked or sent to your junk/spam folder."
    if not Messaging.objects.filter(sender=admin_profile,
                                    receiver=receiver,
                                    comment=message, ).exists():
        Messaging.objects.create(sender=admin_profile,
                                 receiver=receiver,
                                 comment=message, )
    return True


'''
Function   : approve_mentor_twfl
Description: Approve or Reject Mentor profile, Approval is important for mentor to have their public profile page 
Parameters : --
Return     : List system mentor page
'''


@school_admin_user_required
def approve_mentor_twfl(request, admin_slug):
    user = get_object_or_404(Mentor, admin__slug=admin_slug)
    # Update process
    if request.method == 'POST':
        if user.profile_status:
            user.profile_status = False
            user.save()
            print("Mentor profile deactivated......")
            messages.success(request, "Mentor Profile is rejected. You can approve it again from the same page.")
        else:
            user.profile_status = True
            user.save()
            # Get mentor profile url to add it in mail
            # link = getmentorprofileurl(user.admin.slug)
            link = request.build_absolute_uri(reverse('login'))
            send_email_notification.delay('Your Profile is Approved',
                                    'administration/email/mentor_profile_approved.html',
                                    [user.admin.email],
                                    {
                                        'first_name': user.admin.first_name,
                                        'link': link,
                                    }
                                    )
            send_email_notification.delay('New Mentor Profile on International Foundation Group',
                                    'administration/email/standard_template.html', [EMAIL_HOST_USER,],
                                    {
                                        'first_name': 'Team',
                                        'link': link,
                                        'content': 'New Alumnus profile is available on International Foundation Group. Please '
                                                   'Index this Profile URL.',
                                        'button_text': 'View Profile',
                                    }
                                    )
            print("Mentor profile activated......")
            send_greeting_message = greetings_message_twfl(request, user.admin)

            messages.success(request, "Mentor Profile is Updated, Sent email notification.")
        user.save()
    return redirect('administration:list_mentors_twfl')



@school_admin_user_required
def approve_student_twfl(request, admin_slug):
    user = get_object_or_404(Student, admin__slug=admin_slug)
    print("Approval status triggered.....")
    print("Student Approval status - ", user.profile_status)
    # Update process
    if request.method == 'POST':
        if user.profile_status:
            user.profile_status = False
            user.save()
            print("Student profile deactivated......")
            messages.success(request, "Student Profile is rejected. You can approve it again from the same page.")
        else:
            user.profile_status = True
            user.save()
            # Get mentor profile url to add it in mail
            # link = getmentorprofileurl(user.admin.slug)
            link = request.build_absolute_uri(reverse('login'))
            send_email_notification.delay('Your Profile is Approved',
                                    'administration/email/mentor_profile_approved.html',
                                    [user.admin.email],
                                    {
                                        'first_name': user.admin.first_name,
                                        'link': link,
                                    }
                                    )
            send_email_notification.delay('New Student Profile on International Foundation Group',
                                    'administration/email/standard_template.html', [EMAIL_HOST_USER,],
                                    {
                                        'first_name': 'Team',
                                        'link': link,
                                        'content': 'New Student profile is available on International Foundation Group. Please '
                                                   'Index this Profile URL.',
                                        'button_text': 'View Profile',
                                    }
                                    )
            print("Student profile activated......")
            send_greeting_message = greetings_message_twfl(request, user.admin)

            messages.success(request, "Student Profile is Updated, Sent email notification.")
        print("Student Approval status after checkered action - ", user.profile_status)
    return redirect('administration:list_students_twfl')




@super_admin_user_required
def create_unique_url_slug_for_mentor_twfl(request, admin_slug):
    user_pi = MentorPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=admin_slug)
    # Mentor Url Slug update
    count_mentors_with_same_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        admin__name_slug=user_pi.admin.name_slug, currently_studying_slug=user_pi.currently_studying_slug,
        admin__country_slug=user_pi.admin.country_slug, url_slug=user_pi.url_slug)

    if count_mentors_with_same_pi.count() > 1:
        possible_url_slug = ['study-in-' + user_pi.studying_in_slug, 'study-in-the-' + user_pi.studying_in_slug,
                             'study-in-' + user_pi.currently_studying_slug + '-' + user_pi.studying_in_slug,
                             'study-in-' + user_pi.currently_studying_slug + '-the-' + user_pi.studying_in_slug,
                             admin_slug]
        for i in possible_url_slug:
            if MentorPersonalInformation.objects.using('afm_personal_information').filter(
                    admin__name_slug=user_pi.admin.name_slug,
                    currently_studying_slug=user_pi.currently_studying_slug,
                    admin__country_slug=user_pi.admin.country_slug, url_slug=i).exists():
                continue
            else:
                url = i
                user_pi.url_slug = url
                user_pi.save()
                break
    return redirect('administration:mentor_profile', admin_slug)


'''
Function   : change_testimonials_status_is_active_twfl
Description: Approve or Reject Mentor testimonials(Feedbacks), Approval is important for mentor to have their 
             testimonials on public profile page 
Parameters : Mentor testimonial ID (MentorFeedback model)
Return     : List mentor testimonials page
'''


@super_admin_user_required
def change_testimonials_status_is_active_twfl(request, id):
    feedback = get_object_or_404(MentorFeedback, id=id)
    if feedback.status:
        feedback.status = False
    else:
        feedback.status = True
    feedback.save()
    return redirect('administration:list_mentor_testimonials')


'''
Function   : student_profile_twfl
Description: View student profile with his/her information
Parameters : Student/User slug
Return     : Redirect dashboard page
'''


@school_admin_user_required
def student_profile_twfl(request, slug):
    if request.user.user_type == 3:
        slug = request.user.slug
    student_info = Student.objects.get(
        admin__slug=slug)
    student_personal_info = StudentPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=slug)
    return render(request, 'administration/student/student_profile.html',
                  {'student_info': student_info, 'student_personal_info': student_personal_info})



'''
Function   : Parent_profile_twfl
Description: View Parent profile with his/her information
Parameters : Parent/User slug
Return     : Redirect dashboard page
'''


@parent_admin_user_required
def parent_profile_twfl(request, slug):
    if request.user.user_type == 5:
        slug = request.user.slug
    parent_info = Parent.objects.get(
        admin__slug=slug)
    return render(request, 'administration/parent/parent_detail.html',
                  {'parent_info': parent_info})


'''
Function   : mentor_profile_twfl
Description: View Mentor profile with his/her personal information
Parameters : Mentor/User slug
Return     : Redirect mentor details page
'''


@school_admin_user_required
def mentor_profile_twfl(request, slug):
    mentor_info = Mentor.objects.get(
        admin__slug=slug)
    mentor_personal_info = MentorPersonalInformation.objects.using('afm_personal_information').get(
        admin__user_slug=slug)
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=slug)
    form = ProfilePhotoForm(instance=pi_user)
    form2 = MentorUpdateAboutFieldForm(instance=pi_user)
    form3 = MentorUpdateYoutubeShotsFieldForm(instance=mentor_personal_info)
    if request.method == 'POST':
        form = ProfilePhotoForm(
            request.POST, request.FILES, instance=pi_user)
        if form.is_valid():
            form.save()
            return redirect("administration:mentor_profile", slug)
        else:
            messages.error(request, "Invalid form, Profile photo update failed")

    return render(request, 'administration/admin/mentor_profile.html',
                  {'mentor_info': mentor_info, 'mentor_personal_info': mentor_personal_info, 'form': form,
                   'form2': form2, 'form3': form3, 'latepoint_form': LatepointLinkForm(instance=mentor_personal_info)})


'''
Function   : mentor_update_about_me_field_twfl
Description: Update mentor's 'About me' field
Parameters : Mentor/User slug
Return     : Redirect mentor details page
'''


@school_admin_user_required
def mentor_update_about_me_field_twfl(request, slug):
    pi_user = CustomUserPersonalInformation.objects.using(
        'afm_personal_information').get(user_slug=slug)
    if request.method == 'POST':
        form = MentorUpdateAboutFieldForm(request.POST, instance=pi_user)
        if form.is_valid():
            form.save()
            return redirect("administration:mentor_profile", slug)
        else:
            messages.error(request, form.errors)

    return redirect("administration:mentor_profile", slug)


'''
Function   : mentor_update_about_me_field_twfl
Description: Update mentor's 'Youtube shots' field
Parameters : Mentor/User slug
Return     : Redirect mentor details page
'''


@school_admin_user_required
def mentor_update_youtube_shots_field_twfl(request, slug):
    pi_user = MentorPersonalInformation.objects.using(
        'afm_personal_information').get(admin__user_slug=slug)
    if request.method == 'POST':
        form = MentorUpdateYoutubeShotsFieldForm(request.POST, instance=pi_user)
        if form.is_valid():
            form.save()
            return redirect("administration:mentor_profile", slug)
        else:
            messages.error(request, form.errors)

    return redirect("administration:mentor_profile", slug)


'''
Function   : InstituteDetails
Description: Institute Detail page
Parameters : -
Return     : Redirect to institute detail page
'''




class InstituteDetails(DetailView):
    model = CustomUser
    fields = ('email',)
    template_name = ('administration/institute_detail.html')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        institute = context['object']
        context['institute_object'] = Institute.objects.get(
            admin__slug=institute.slug)
        return context


'''
Function   : InstituteDetails
Description: Institute Detail page
Parameters : -
Return     : Redirect to institute detail page
'''


@super_admin_user_required
def institute_update(request, pk):
    inst_obj = Institute.objects.get(admin__pk=pk)
    institute_detail = get_object_or_404(CustomUser, pk=pk)
    institute_scholarship_detail = get_object_or_404(Institute, id=inst_obj.id)
    form = InstituteUpdateForm(instance=institute_detail)
    form2 = InstituteScholarshipForm(instance=institute_scholarship_detail)
    if request.method == 'POST':
        form = InstituteUpdateForm(request.POST, instance=institute_detail)
        form2 = InstituteScholarshipForm(
            request.POST, instance=institute_scholarship_detail)
        if form.is_valid() and form2.is_valid():
            # if form2.is_valid():
            user_obj = form.save(commit=False)
            user_obj.username = user_obj.email
            user_obj.save()
            form2.save()
            return redirect('administration:list_institutes_twfl')
        else:
            print(form.errors)
    return render(request, "administration/institute_update.html", {'form': form, 'form2': form2, 'inst_obj': inst_obj})


@super_admin_user_required
def delete_institute_profile_pic(request, id):
    pic = CustomUser.objects.get(id=id)
    pic.profile_pic.delete()
    return redirect('administration:institute_information_edit', id)


@super_admin_user_required
def update_profile_pic_institute(request, pk):
    user = CustomUser.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateProfilePicForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('administration:institute_information_edit', pk)
        else:
            print(form.errors)


class InstituteDelete(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('administration:list_institutes_twfl')


from django.views.decorators.csrf import csrf_exempt

'''
Function   : MentorLatepointLink
Description: Submit mentor's latepoint booking link
Parameters : Mentor_id
Return     : Redirect to mentors list page
'''


@csrf_exempt
@school_admin_user_required
def MentorLatepointLink(request, id):
    user = MentorPersonalInformation.objects.get(id=id)
    if request.method == 'POST':
        form = LatepointLinkForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "ApplyPeer link is updated")
            return redirect('administration:list_mentors_twfl')
        else:
            print(form.errors)
            messages.error(
                request, "Enter a valid url")
            return redirect('administration:list_mentors_twfl')


'''
Function   : admin_meeting_link
Description: Submit Admin's meeting link
Parameters : Mentor_id
Return     : Redirect to mentors list page
'''


@csrf_exempt
def admin_meeting_link(request):
    admin_user = Admin.objects.first()
    if request.method == 'POST':
        form = AdminMeetingLinkForm(request.POST, instance=admin_user or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Meeting links are updated")
            return redirect('administration:dashboard')
        else:
            print(form.errors)
            messages.error(request, "Enter a valid url")
            return redirect('administration:dashboard')


'''
Function   : mentor_subscribe_twfl
Description: Student/Parent can Subscribe to mentor profile and send email notification
Parameters : --
Return     : Redirect to current page
'''


def mentor_subscribe_twfl(request):
    if request.method == 'POST':
        # Get guest user's email id
        email = request.POST['email']
        # Get mentor-slug guest user willing to subscribe to
        mentor_slug = request.POST['mentor-slug']
        # Get current page url
        redirect_url = request.POST['redirect-url']
        # Get mentor object
        mentor = get_object_or_404(Mentor, admin__slug=mentor_slug)
        # Get mentor personal-information
        mentor_pi = get_object_or_404(MentorPersonalInformation, admin__user_slug=mentor_slug)
        # Check if user is already subscribed
        if not Subscriber.objects.filter(subscribe_to=mentor, email=email).exists():
            Subscriber.objects.create(subscribe_to=mentor, email=email)
            html_message = loader.render_to_string('email/subscriber.html', {
                'mentor_pi': mentor_pi,
                'title': 'Thank you for subscribing to future blogs by Mentor %s.' % (mentor_pi.admin.first_name),
            })
            try:
                # Send email notification
                mail = send_mail('Thank you for Subscribing', "Hello", None, [email],
                                 html_message=html_message)
                message = "success"
            except SMTPException as e:
                print(f'error  : {e}')
                message = e
            else:
                message = "Mail could not be sent, Please contact administrator"
            messages.success(request, "Thank you for subscribing to my future blogs")
        else:
            messages.success(request, "You are already subscribed to this mentor")
        return redirect(redirect_url)
    else:
        messages.error(request, "Invalid Request")
        return redirect('administration:home')


'''
Function   : delete_user_twfl
Description: Delete user and their personal information if exists.
Parameters : User slug
Return     : Redirect to current page
'''


@super_admin_user_required
def delete_user_twfl(request, user_slug):
    # Get current page url
    redirect_link = request.POST['redirect']
    user_personal_pi = None
    if request.method == 'POST':
        user_object = CustomUser.objects.get(slug=user_slug)
        # Check if user is mentor, Mentor user type is 4
        if user_object.user_type == 4:
            # Get mentor personal information object from Database 2(Personal Information)
            user_personal_pi = CustomUserPersonalInformation.objects.get(user_slug=user_slug)
        # Check if user is student, Student user type is 3
        if user_object.user_type == 3:
            # Get mentor personal information object from Database 2(Personal Information)
            user_personal_pi = CustomUserPersonalInformation.objects.get(user_slug=user_slug)
        user_object.delete()
        if user_personal_pi:
            user_personal_pi.delete()
        messages.success(
            request, "User Successfully Removed")
    return redirect(redirect_link)


'''
Function   : contact_us_twfl
Description: Contact us page with form integration, Send email to admin 
Parameters : --
Return     : Redirect to contact page
'''


def contact_us_twfl(request):
    form = ContactUsForm()
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            contact = form.save()
            var_dict = {'name': contact.name,
                        'i_am_a': contact.i_am_a,
                        'country_name': contact.country.name,
                        'email': contact.email,
                        'phone_no': str(contact.phone_no),
                        'subject': contact.subject,
                        'question1': contact.question1,
                        'message': contact.message,
                        'title': 'New Contact lead from',
                        }
            if contact.admin:
                var_dict['admin'] = contact.admin
                var_dict['admin_first_name'] = contact.admin.first_name
                var_dict['admin_slug'] = contact.admin.slug

            response = send_email_notification.delay('New Contact Lead',
                                               'administration/email/contact_mail.html',
                                               [mail_send_from],
                                               var_dict
                                               )
            if response:
                messages.success(
                    request, "We received your request, we will get back to you shortly.")
            else:
                messages.error(
                    request, "Failed to send email, please use our email id to contact us, Thank you.")
            # # Prepare email template
            # html_message = loader.render_to_string('administration/email/contact_mail.html', {
            #     'contact': instance,
            #     'title': 'New Contact lead from',
            # })
            # try:
            #     # Send email
            #     mail = send_mail('New Contact Lead', "Hello", None, [mail_send_from],
            #                      html_message=html_message)
            #     message = "success"
            #     messages.success(
            #         request, "We received your request, we will get back to you shortly.")
            # except SMTPException as e:
            #     print(f'error  : {e}')
            #     message = e
            #     messages.error(
            #         request, "Mail could not be sent.")
            # else:
            #     message = "Mail could not be sent, Please contact administrator"
        else:
            messages.error(request, "Invalid Data")
    return render(request, 'website/contact.html', {'form': form, })


'''
Function   : demand_n_supply 
Description: Demand is a required number of mentors available for a category of students. Category includes
             Spoken languages, country and subject.
Parameters : --
Return     : Return list of demands of mentors for registered students
'''


@super_admin_user_required
def demand_n_supply(request):
    mentor_qset = MentorPersonalInformation.objects.all()
    student_qset = StudentPersonalInformation.objects.all()
    dns_qset = DemandAndSupply.objects.all()

    for i in mentor_qset:
        for j in i.admin.spoken_languages.all():
            language = j.language
            country = i.studying_in
            subject = i.currently_studying
            get_dns = DemandAndSupply.objects.filter(spoken_language=language, country=country, subject=subject).count()
            if get_dns == 0:
                DemandAndSupply.objects.create(spoken_language=language, country=country, subject=subject)

    for i in student_qset:
        for j in i.admin.spoken_languages.all():
            for k in i.study_destination:
                language = j
                country = k
                subject = i.area_of_study
                get_dns = DemandAndSupply.objects.filter(spoken_language=language, country=country,
                                                         subject=subject).count()
                if get_dns == 0:
                    DemandAndSupply.objects.create(spoken_language=language, country=country, subject=subject)

    for i in dns_qset:
        mentor = MentorPersonalInformation.objects.filter(admin__spoken_languages__language=i.spoken_language,
                                                          studying_in=i.country, currently_studying=i.subject).count()
        student = StudentPersonalInformation.objects.filter(admin__spoken_languages__language=i.spoken_language,
                                                            study_destination__contains=i.country,
                                                            area_of_study=i.subject).count()
        i.demand = student
        i.supply = mentor
        i.save()

    return redirect('administration:dns_list')


class DemandAndSupplyList(ListView):
    model = DemandAndSupply

    def get_context_data(self, **kwargs):
        context = super(DemandAndSupplyList, self).get_context_data(**kwargs)
        filtered_qs = DemandAndSupplyFilter(self.request.GET,
                                            queryset=DemandAndSupply.objects.all().order_by('-created_at'))
        context['filter'] = filtered_qs
        paginated_filter = Paginator(filtered_qs.qs, 10)
        page_number = self.request.GET.get('page')
        context['page_obj'] = paginated_filter.get_page(page_number)
        return context






def ajax_google_slug_session(request):
    slug = request.GET.get("slug")
   
    # Create session
    request.session['chatslug'] = slug
    session_slug = request.session['chatslug']
    print("--------------------------- Chat Session slug ----------------------------")
    print("Incoming Slug - ", slug)
    print("Chat Session Value - ", request.session['chatslug'])

    return JsonResponse({"success": 200, 'session_slug':session_slug})





# -------------------------------------------------------------
# WEB NOTIFICATIONS
# -------------------------------------------------------------

'''
Function   : test_web_notification 
Description: Generate web notification for testing purpose
Parameters : --
Return     : create web notification 
'''


def test_web_notification(request):
    # Send Notification
    payload = {
        "head": request.user.first_name + " sent you a message",
        "body": "Test message",
        # "icon": "https://tag-afm-bucket.s3.amazonaws.com/static/images/default_profile.png",
        # "url": config('AFM_LINK') + "/messages-list/",
    }
    send_user_notification(user=request.user, payload=payload, ttl=1000)
    return redirect("administration:dashboard")


# -------------------------------------------------------------
# STATIC WEBSITE PAGES
# -------------------------------------------------------------

# ---------------------Not in USE------------------------------

def medical_school_mentor_twfl(request):
    return render(request, 'website/medical-school-mentor.html')


def uk_medical_schools_twfl(request):
    return render(request, 'website/uk-medical-schools/index.html')


def widening_access_twfl(request):
    return render(request, 'website/uk-medical-schools/widening-access.html')


def studying_medicine_at_anglia_ruskin_university_twfl(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-anglia-ruskin-university.html')


def study_medicine_twfl(request):
    return render(request, 'website/study-medicine.html')


def studying_medicine_at_aston_university_twfl(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-aston-university.html')


def studying_medicine_at_barts_twfl(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-barts.html')


def studying_medicine_at_brighton_and_sussex_medical_school_twfl(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-brighton-and-sussex-medical-school.html')


def studying_medicine_at_brunel_university_london_twfl(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-brunel-university-london.html')


def study_medicine_in_australia_twfl(request):
    return render(request, 'website/study-medicine-in-australia/index.html')


def study_medicine_in_ireland_twfl(request):
    return render(request, 'website/study-medicine-in-ireland/index.html')


def study_medicine_in_the_caribbean_twfl(request):
    return render(request, 'website/study-medicine-in-the-caribbean/index.html', {'form': UniversityContactUsForm()})


def study_medicine_in_canada_twfl(request):
    return render(request, 'website/study-medicine-in-canada/index.html')


def study_medicine_in_the_usa_twfl(request):
    return render(request, 'website/study-medicine-in-the-usa/index.html')


# ---------------- Medical schools in Europe ----------------

def medical_schools_in_europe_twfl(request):
    return render(request, 'website/medical-schools-in-europe/index.html', {'form': UniversityContactUsForm()})


def university_contact_form(request):
    redirect_link = request.POST['redirect']
    if request.method == 'POST':
        return redirect(redirect_link)
        form = UniversityContactUsForm(request.POST)
        if form.is_valid():
            instance = form.save()
            html_message = loader.render_to_string('administration/email/contact_mail.html',
                                                   {
                                                       'contact': instance,
                                                       'title': 'New Contact lead from',
                                                   })
            try:
                mail = send_mail('New Contact Lead', "Hello", None, [mail_send_from],
                                 html_message=html_message)
                message = "success"
            except SMTPException as e:
                print(f'error  : {e}')
                message = e
            else:
                message = "Mail could not be sent, Please contact administrator"
            messages.success(
                request, "We received your request, we will get back to you shortly.")
        else:
            print(form.errors)
            messages.error(request, "Invalid Form")
    return redirect(redirect_link)


def studying_medicine_at_karolinska_institute_twfl(request):
    return render(request, 'website/medical-schools-in-europe/studying-medicine-at-karolinska-institute.html')


def studying_medicine_at_charles_university_twfl(request):
    return render(request, 'website/medical-schools-in-europe/studying-medicine-at-charles-university.html')


def studying_medicine_at_medical_university_sofia_twfl(request):
    return render(request, 'website/medical-schools-in-europe/studying-medicine-at-medical-university-sofia.html')


def studying_medicine_at_the_medical_university_of_silesia_twfl(request):
    return render(request,
                  'website/medical-schools-in-europe/studying-medicine-at-the-medical-university-of-silesia.html')


# ---------------- Study medicine in Ireland ----------------

def studying_medicine_at_national_university_of_ireland_twfl(request):
    return render(request, 'website/study-medicine-in-ireland/studying-medicine-at-national-university-of-ireland.html')


def studying_medicine_at_royal_college_of_surgeons_twfl(request):
    return render(request, 'website/study-medicine-in-ireland/studying-medicine-at-royal-college-of-surgeons.html')


def studying_medicine_at_trinity_college_dublin_twfl(request):
    return render(request, 'website/study-medicine-in-ireland/studying-medicine-at-trinity-college-dublin.html')


def studying_medicine_at_university_college_cork_ucc_twfl(request):
    return render(request, 'website/study-medicine-in-ireland/studying-medicine-at-university-college-cork-ucc.html')


def studying_medicine_at_university_college_dublin_twfl(request):
    return render(request, 'website/study-medicine-in-ireland/studying-medicine-at-university-college-dublin.html')


def studying_medicine_at_university_of_limerick_twfl(request):
    return render(request, 'website/study-medicine-in-ireland/studying-medicine-at-university-of-limerick.html')


# ---------------- UK medical schools ----------------

def studying_medicine_at_newcastle_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-newcastle-university.html')


def studying_medicine_at_the_university_of_exeter(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-exeter.html')


def studying_medicine_at_norwich_medical_school(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-norwich-medical-school.html')


def studying_medicine_at_the_university_of_glasgow(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-glasgow.html')


def studying_medicine_at_anglia_ruskin_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-anglia-ruskin-university.html')


def studying_medicine_at_peninsula_medical(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-peninsula-medical.html')


def studying_medicine_at_the_university_of_leeds(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-leeds.html')


def studying_medicine_at_aston_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-aston-university.html')


def studying_medicine_at_queens_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-queens-university.html')


def studying_medicine_at_the_university_of_leicester(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-leicester.html')


def studying_medicine_at_barts(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-barts.html')


def studying_medicine_at_royal_college_of_surgeons(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-royal-college-of-surgeons.html')


def studying_medicine_at_the_university_of_lincoln(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-lincoln.html')


def studying_medicine_at_brighton_and_sussex_medical_school(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-brighton-and-sussex-medical-school.html')


def studying_medicine_at_st_georges_university_of_london(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-st-georges-university-of-london.html')


def studying_medicine_at_the_university_of_liverpool(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-liverpool.html')


def studying_medicine_at_brunel_university_london(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-brunel-university-london.html')


def studying_medicine_at_swansea_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-swansea-university.html')


def studying_medicine_at_the_university_of_nottingham(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-nottingham.html')


def studying_medicine_at_cardiff_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-cardiff-university.html')


def studying_medicine_at_the_university_college_london_ucl(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-college-london-ucl.html')


def studying_medicine_at_the_university_of_oxford(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-oxford.html')


def studying_medicine_at_edge_hill_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-edge-hill-university.html')


def studying_medicine_at_the_university_of_aberdeen_school_of_medicine(request):
    return render(request,
                  'website/uk-medical-schools/studying-medicine-at-the-university-of-aberdeen-school-of-medicine.html')


def studying_medicine_at_the_university_of_sheffield(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-sheffield.html')


def studying_medicine_at_hull_york_medical_school(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-hull-york-medical-school.html')


def studying_medicine_at_the_university_of_birmingham(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-birmingham.html')


def studying_medicine_at_the_university_of_southampton(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-southampton.html')


def studying_medicine_at_imperial_college_london(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-imperial-college-london.html')


def studying_medicine_at_the_university_of_bristol(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-bristol.html')


def studying_medicine_at_the_university_of_st_andrews(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-st-andrews.html')


def studying_medicine_at_keele_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-keele-university.html')


def studying_medicine_at_the_university_of_buckingham(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-buckingham.html')


def studying_medicine_at_the_university_of_sunderland(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-sunderland.html')


def studying_medicine_at_kent_and_medway_medical_school(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-kent-and-medway-medical-school.html')


def studying_medicine_at_the_university_of_cambridge(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-cambridge.html')


def studying_medicine_at_ulster_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-ulster-university.html')


def studying_medicine_at_kings_college_london_kcl(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-kings-college-london-kcl.html')


def studying_medicine_at_the_university_of_central_lancashire_uclan(request):
    return render(request,
                  'website/uk-medical-schools/studying-medicine-at-the-university-of-central-lancashire-uclan.html')


def studying_medicine_at_warwick(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-warwick.html')


def studying_medicine_at_lancaster_university(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-lancaster-university.html')


def studying_medicine_at_the_university_of_dundee(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-dundee.html')


def studying_medicine_at_manchester(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-manchester.html')


def studying_medicine_at_the_university_of_edinburgh(request):
    return render(request, 'website/uk-medical-schools/studying-medicine-at-the-university-of-edinburgh.html')


@super_admin_user_required
def test_link_list_mentors_twfl(request):
    if request.method != 'POST':
        # Get all mentors from Database1
        mentors = Mentor.objects.all().order_by('profile_status')
        queryset = MentorPersonalInformation.objects.using('afm_personal_information').all().order_by('-created_at')
        # filtered_qs = MentorFilter(request.GET, queryset)
        # paginated_filtered = Paginator(filtered_qs.qs, 50)
        # page_number = request.GET.get('page')
        # page_obj = paginated_filtered.get_page(page_number)

        return render(request, 'administration/admin/link_list_mentors.html',
                      {'mentors': mentors, 'personal_info_list': queryset, })


def redirect_blog_url(request):
    return redirect('blogs:PostDetail', 'medicine-is-personal-to-each-applicant')


@super_admin_user_required
def import_user_twfl(request):
    users_to_import = UserCSVImportedData.objects.filter(is_imported=False)
    for user_data in users_to_import:
        user_object, created = CustomUser.objects.get_or_create(username=user_data.email, email=user_data.email, )
        if user_object:
            user_object.first_name = user_data.first_name
            user_object.last_name = user_data.last_name
            if not user_object.password:
                user_object.set_password('Admin@123')
            user_object.save()
            # if imported user is student
            if user_data.user_type.lower() == 'student':
                user_object.user_type = 3
                user_object.save()
                student_object, created = Student.objects.get_or_create(admin=user_object, school=SCHOOL_OBJECT)
                if student_object:
                    student_object.currently_studying_course = user_data.currently_studying_course
                    student_object.save()

                if CustomUserPersonalInformation.objects.using('afm_personal_information').filter(
                        user_slug=user_object.slug).exists():
                    user_pi_object = CustomUserPersonalInformation.objects.using('afm_personal_information').get(
                        user_slug=user_object.slug)
                    user_pi_object.first_name = user_object.first_name
                    user_pi_object.last_name = user_object.last_name
                    user_pi_object.save()

                else:
                    user_pi_object, created = CustomUserPersonalInformation.objects.using('afm_personal_information').get_or_create(
                        user_slug=user_object.slug,
                        first_name=user_object.first_name,
                        last_name=user_object.last_name)
                if user_pi_object:
                    StudentPersonalInformation.objects.using('afm_personal_information').get_or_create(
                        admin=user_pi_object)

                app, created = Application.objects.get_or_create(admin=user_object)
                if app:
                    EnglishLanguage.objects.get_or_create(app=app)
                    VisaHistory.objects.get_or_create(app=app)
                    ApplicationFeedback.objects.get_or_create(app=app)
                    Reference.objects.get_or_create(app=app)
                    ProfessionalExperience.objects.get_or_create(app=app)
                    ProfessionalTrainingCertificate.objects.get_or_create(app=app)
                    AcademicQualification.objects.get_or_create(app=app)
                    PersonalStatement.objects.get_or_create(app=app)

                    # Create blank object In personal information database
                    app_pi, created = AppBasicInformation.objects.using('afm_personal_information').get_or_create(
                        app=app.id,
                        user_slug=user_object.slug,
                        email=user_data.email)
                    if app_pi:
                        app_pi.first_name = user_data.first_name
                        app_pi.surname = user_data.last_name
                        app_pi.date_of_birth = user_data.date_of_birth
                        app_pi.nationality = user_data.nationality
                        app_pi.mobile_number = user_data.phone
                        app_pi.save()
                        AppAddress.objects.using('afm_personal_information').get_or_create(app=app_pi)
                        AppPassportInformation.objects.using('afm_personal_information').get_or_create(app=app_pi)

                user_data.is_imported = True
                user_data.save()

            # If user is a Mentor
            elif user_data.user_type.lower() == 'alumni':
                user_object.user_type = 4
                user_object.save()

                Mentor.objects.get_or_create(admin=user_object, school=SCHOOL_OBJECT)
                if CustomUserPersonalInformation.objects.using('afm_personal_information').filter(
                        user_slug=user_object.slug).exists():
                    user_pi_object = CustomUserPersonalInformation.objects.using('afm_personal_information').get(
                        user_slug=user_object.slug)
                    user_pi_object.first_name = user_object.first_name
                    user_pi_object.last_name = user_object.last_name
                else:
                    user_pi_object, created = CustomUserPersonalInformation.objects.using('afm_personal_information').get_or_create(
                        user_slug=user_object.slug,
                        first_name=user_object.first_name,
                        last_name=user_object.last_name)
                MentorPersonalInformation.objects.using('afm_personal_information').get_or_create(admin=user_pi_object)

                user_pi_object.country = user_data.nationality
                user_pi_object.phone = user_data.phone
                user_pi_object.date_of_birth = user_data.date_of_birth
                if user_data.languages:
                    languages = user_data.languages.replace(" ", "")
                    languages_list = languages.split(",")
                    for i in languages_list:
                        if SpokenLanguage.objects.filter(language=i).exists():
                            language_obj = SpokenLanguage.objects.filter(language=i).first()
                            user_pi_object.spoken_languages.add(SpokenLanguage.objects.get(id=language_obj.id))

                user_pi_object.save()

                user_data.is_imported = True
                user_data.save()

            # If user type is Parent get_or_create Null objects for relative models
            elif user_data.user_type.lower() == 'parent':
                user_object.user_type = 5
                user_object.save()
                Parent.objects.get_or_create(admin=user_object)

                user_data.is_imported = True
                user_data.save()

            # If user is a Future Student
            elif user_data.user_type.lower() == 'future student':
                user_object.user_type = 12
                user_object.save()
                FutureStudent.objects.get_or_create(admin=user_object, school=SCHOOL_OBJECT)

                user_data.is_imported = True
                user_data.save()
        else:
            messages.error(request, "Failed to import user!")
    return redirect('administration:import_data')


from django.shortcuts import render
from import_export.formats import base_formats
from .resources import UserCSVImportedDataResource
from tablib import Dataset


@super_admin_user_required
def import_data(request):
    users_to_import_exists = UserCSVImportedData.objects.filter(is_imported=False).exists()
    queryset = UserCSVImportedData.objects.all()
    queryset = UserCSVImportedDataFilter(request.GET, queryset)
    paginated_filtered = Paginator(queryset.qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    if request.method == 'POST' and request.FILES.get('file'):
        dataset = Dataset()  # Create a Tablib Dataset
        file_data = request.FILES['file'].read().decode('utf-8')
        dataset.csv = file_data  # Load the file data into the Dataset
        resource = UserCSVImportedDataResource()
        result = resource.import_data(dataset, dry_run=False, raise_errors=True)
        # Handle the import result as needed (e.g., show success/failure message
        messages.success(request, "Data is imported successfully!")
        return redirect('administration:import_data')
    # else:
        # messages.error(request, "Failed to import user!")

    return render(request, 'administration/admin/import_template.html',
                  {'users_to_import': page_obj, 'form': queryset.form,
                   'page_obj': page_obj, 'users_to_import_exists': users_to_import_exists})