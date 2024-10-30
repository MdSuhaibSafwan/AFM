import json
from decouple import config
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.serializers import serialize
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from AFM.settings import MAIL_SEND_FROM
from administration.login_check import admin_user_required, student_parent_admin_user_required, \
    student_parent_institute_login_required, parent_admin_user_required, super_admin_user_required, institute_user_required, \
    student_user_required, student_parent_school_admin_user_required
from administration.models import Institute, BlockUser, AdditionalQuestions
from application.models import Application, AcademicQualification, EnglishLanguage, ProfessionalExperience, \
    Reference, PersonalStatement, VisaHistory, ProfessionalTrainingCertificate, ApplicationOfferStatus, \
    ApplicationComment, DirectApplication, ApplicationAppliedAtUniversityLogin, ConsideredApplication, \
    DocumentUpload, FinalSelected, ApplicationFeedback
from notifications.models import Notification
from personal_information.models import AppBasicInformation, AppAddress, AppPassportInformation, \
    CustomUserPersonalInformation, StudentPersonalInformation
from application.forms import ApplicationForm, AppBasicInformationForm, AppAddressForm, \
    AppPassportInformationForm, AppEducationForm, AppEnglishLanguageForm, AppWorkExperienceForm, \
    app_references_form, AppPersonalStatementForm, AppVisaHistoryForm, AppAdditionalInformationForm, \
    AppInstituteFeedbackForm, AppCommentForm, AppTrainingCertificatesForm, DirectApplicationsForm, \
    AppAdditionalDocumentsForm, AppInstituteRejectForm, SelectMentorForm, OfferFinalSelection, AppBasicEducationForm, \
    ApplicationFeedbackForm, NextOfKinInformationForm, WouldYouLikeOurAlumniToAssistYouInEnglishSkillsForm, \
    WouldYouLikeGainAdditionalWorkExperience, WouldYouBeInterestedInSharingYourDetailsWithInstitute
from application.filters import ApplicationFilter
from notifications.signals import notify
import datetime
from django.template import loader
from smtplib import SMTPException
from AFM.tasks import send_email_notification
from django.db.models import Q
from django.template.loader import get_template
import pdfkit
from django.templatetags.static import static
mail_send_from = MAIL_SEND_FROM


'''
Function   : delete_null_application_instance_twfl
Description: Delete all null application created
Parameters : --
Return     : Delete applications
'''

def delete_null_application_instance_twfl(request):
    trash = Application.objects.filter(admin=request.user, status=None)
    if trash:
        for instance in trash:
            trash_pi = AppBasicInformation.objects.using('afm_personal_information').filter(app=instance.id)
            print(instance.id)
            trash_pi.delete()
            instance.delete()


'''
Date       : 12/21/2020 
Function   : application_consent_twfl
Description: Student application consent form
Parameters : Application slug
Return     : On successful submission redirect to next form 
'''

@student_parent_admin_user_required
def application_consent_twfl(request, app_slug):
    # Get Application object
    app = Application.objects.get(slug=app_slug or None, admin=request.user)
    basic_info = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id,
                                                                                   user_slug=request.user.slug)
    # Check if user has already filled the forms or not by checking form status
    # if AcademicQualification.objects.filter(app=app.id).exists():
    #     if AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is not None:
    #         return redirect("application:view_application_twfl", app.slug)

    # if app.status not in [None, 1, 3]:
    #     return redirect("application:review_submit_twfl", app.slug)

    direct_application_formset = modelformset_factory(ConsideredApplication, form=DirectApplicationsForm, extra=1,
                                                      max_num=1)
    formset_direct_application = direct_application_formset(request.POST or None,
                                                            queryset=ConsideredApplication.objects.filter(app=app))
    # context = {}
    # Check if user is student, student user type is 3
    # if request.user.user_type == 3:
        # Get personal information from database 2 (Personal Information)
        # pi_user = StudentPersonalInformation.objects.using('afm_personal_information').get(
        #     admin__user_slug=request.user.slug)
        # if app.program_level is None:
        #     context['program_level'] = pi_user.programme_level
        # if app.subject is None:
        #     context['subject'] = pi_user.area_of_study
        # if app.study_destination_country is None:
        #     context['study_destination_country'] = pi_user.study_destination

    app_form = ApplicationForm(request.POST or None, instance=basic_info,
                               # initial=context
                               )
    if app_form.is_valid():
        app_form.save()

        # Application Status:
        # (0, 'Approved'),
        # (1, 'Rejected'),
        # (2, 'Completed'),
        # (3, 'Incomplete'),

        # Send email to application email
        # sent_email = False
        # if app.status is None:
        #     sent_email = True

        app.status = 3
        app.submitted_at = datetime.datetime.now()
        # Check if user is Parent, Parent user type is 5
        if request.user.user_type == 5:
            app.consent_as_parent = True
        app.save()
        # instances = formset_direct_application.save(commit=False)

        # Check if user has selected multiple institutes
        # for instance in instances:
        #     if ConsideredApplication.objects.filter(institute=instance.institute, app=app).exists():
        #         messages.error(request, "Please select different institutes")
        #         return redirect("application:application_consent_twfl", app.slug)
        #     # In-case NULL entry has added
        #     if not instance.institute:
        #         direct_apps = ConsideredApplication.objects.filter(app=app, is_direct_app=True)
        #         instance.delete()
        #         # if direct_apps:
        #         #     for direct_app in direct_apps:
        #         #         direct_app.delete()
        #     else:
        #         instance.app = app
        #         # Application for selected Institute will get considered as direct application
        #         instance.is_direct_app = True
        #         instance.save()
        # Send email to admin email
        # if sent_email:
        #     link = ''.join(
        #         [config('AFM_LINK'), '/application/application/', str(app.slug)])
        #     send_email_notification.delay('Notification from TAG',
        #                                   'application/notification_mail.html',
        #                                   [mail_send_from],
        #                                   {
        #                                       'link': link,
        #                                       'msg': 'We received an application request.',
        #                                   }
        #                                   )
        # Delete all the junk applications
        delete_null_application_instance_twfl(request)
        return redirect("application:application_personal_information_twfl", app.slug)
    else:
        print(app_form.errors)
        # print(formset_direct_application.errors)
    return render(request, "application/application_consent.html",
                  {'form': app_form, 'app': app,
                   'formset': formset_direct_application
                   })


'''
Date       : 12/22/2020
Function   : application_personal_information_twfl
Description: Personal Information application form, data will be saved in "afm-personal-information" database
Parameters : Application ID
Return     : On successful submission redirect to next form 
'''


@student_parent_admin_user_required
def application_personal_information_twfl(request, app_slug):
    context = {}
    app = Application.objects.get(slug=app_slug, admin=request.user)

    # Check if user has already filled the forms or not by checking form status
    # if AcademicQualification.objects.filter(app=app.id).exists():
    #     if AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is not None:
    #         return redirect("application:view_application_twfl", app.slug)
    basic_info = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id,
                                                                                   user_slug=request.user.slug)
    # Application Status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    # if app.status is None:
    #     return redirect("application:application_consent_twfl", app.slug)
    # Check if user has already filled the form or not by checking form status
    # if app.status in [0, 2]:
    #     return redirect("application:view_application_twfl", app.slug)
    address = AppAddress.objects.using('afm_personal_information').get(app=basic_info)

    # Check if user is student, student user type is 3
    if request.user.user_type == 3:
        # Get personal information from database 2 (Personal Information)
        pi_user = CustomUserPersonalInformation.objects.using('afm_personal_information').get(
            user_slug=request.user.slug)
        if basic_info.date_of_birth is None:
            context['date_of_birth'] = pi_user.date_of_birth
        if basic_info.gender is None:
            context['gender'] = pi_user.gender
        if not basic_info.native_languages.exists():
            context['native_languages'] = [i.id for i in pi_user.spoken_languages.all()]

    if request.method != "POST":
        basic_info_form = AppBasicInformationForm(instance=basic_info, initial=context)
        address_form = AppAddressForm(instance=address)

    else:
        basic_info_form = AppBasicInformationForm(request.POST, instance=basic_info)
        address_form = AppAddressForm(request.POST, instance=address)

        if basic_info_form.is_valid() and address_form.is_valid():
            ob = basic_info_form.save(commit=False)
            ob.save(using='afm_personal_information')
            basic_info_form.save_m2m()
            ob2 = address_form.save(commit=False)
            ob2.save(using='afm_personal_information')
            return redirect("application:application_education_twfl", app.slug)

        else:
            print(basic_info_form.errors)
            print(address_form.errors)
            messages.error(request, "Failed to save, Form is not valid")
    return render(request, 'application/application_personal_information.html',
                  {'basic_info_form': basic_info_form, 'address_form': address_form, 'app': app})


'''
Date       : 12/22/2020
Function   : application_education_twfl
Description: Multiple Education details form
Parameters : Application ID
Return     : On successful submission redirect to next form 
'''

@student_parent_admin_user_required
def application_education_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)
    # Check if user has already filled the forms or not by checking form status
    # if AcademicQualification.objects.filter(app=app.id).exists():
    #     if AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is not None:
    #         return redirect("application:view_application_twfl", app.slug)
    # Application Status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    basic_info = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id,
                                                                                   user_slug=request.user.slug)

    # if basic_info.title is None:
    #     return redirect("application:application_consent_twfl", app.slug)

    # Check if user has already filled the form or not by checking form status
    # if app.status in [0, 2]:
    #     return redirect("application:view_application_twfl", app.slug)

    education_Formset = modelformset_factory(AcademicQualification, form=AppEducationForm, extra=0,
                                             # can_delete=True
                                             )
    if request.method == 'POST':
        formset_education = education_Formset(request.POST, request.FILES)
        basic_education = AppBasicEducationForm(request.POST, instance=basic_info)
        if basic_education.is_valid() and formset_education.is_valid():
            # instances = formset_education.save(commit=False)
            for instance in formset_education:
                obj = instance.save(commit=False)
                obj.app = app
                if 'specify_qualification_name' in instance.cleaned_data:
                    if instance.cleaned_data['specify_qualification_name'] != 'Other':
                        obj.qualification_achieved = instance.cleaned_data['specify_qualification_name']
                obj.save()
            basic_education.save()
            return redirect('application:application_training_twfl', app.slug)
        else:
            print(formset_education.errors)
            print(basic_education.errors)
    else:
        basic_education = AppBasicEducationForm(instance=basic_info)
        formset_education = education_Formset(queryset=AcademicQualification.objects.filter(app=app.id))
    return render(request, 'application/application_education.html',
                  {'formset': formset_education, 'basic_education_form':basic_education,  'app': app})


'''
Date       : 12/22/2020
Function   : application_training_twfl 
Description: Multiple training details form
Parameters : Application ID
Return     : On successful submission redirect to next form 
'''

@student_parent_admin_user_required
def application_training_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)

    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #     return redirect("application:view_application_twfl", app.slug)

    training_Formset = modelformset_factory(ProfessionalTrainingCertificate, form=AppTrainingCertificatesForm,
                                            extra=0)
    if request.method == 'POST':
        formset_training = training_Formset(request.POST, request.FILES)
        if formset_training.is_valid():
            instances = formset_training.save(commit=False)
            for instance in instances:
                instance.app = app
                instance.save()

            return redirect('application:application_english_language_twfl', app.slug)
        else:
            print(formset_training.errors)
    else:
        # messages.error(request, "Failed to save, Form is not valid")
        formset_training = training_Formset(queryset=ProfessionalTrainingCertificate.objects.filter(app=app.id))
    return render(request, 'application/application_training.html',
                  {'formset_training': formset_training, 'app': app})


'''
Date       : 12/23/2020 
Function   : application_english_language_twfl
Description: Add english language certificate in application form
Parameters : Application ID
Return     : On successful submission redirect to next form - work experience
'''


@student_parent_admin_user_required
def application_english_language_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)

    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #     return redirect("application:view_application_twfl", app.slug)

    english_lan_app = EnglishLanguage.objects.get(app=app)
    if request.method != "POST":
        form = AppEnglishLanguageForm(instance=english_lan_app)
        form2 = WouldYouLikeOurAlumniToAssistYouInEnglishSkillsForm(instance=app)
        return render(request, 'application/application_english_language.html', {'form': form, 'form2': form2,
                                                                                 'app': app})
    else:
        form = AppEnglishLanguageForm(request.POST, request.FILES, instance=english_lan_app)
        form2 = WouldYouLikeOurAlumniToAssistYouInEnglishSkillsForm(request.POST, instance=app)
        if form.is_valid() and form2.is_valid():
            form.save()
            form2.save()
            return redirect("application:application_work_experience_twfl", app.slug)

        else:
            print(form.errors)
            print(form2.errors)
            messages.error(request, "Failed to save, Form is not valid")
            return render(request, "application/application_english_language.html", {'form': form, 'form2':form2,
                                                                                     'app': app})


'''
Author     : Viral Solanki 
Date       : 12/23/2020 
Function   : application_work_experience_twfl
Description: Add work experience in application form
Parameters : Application ID
Return     : On successful submission redirect to references form 
'''

@student_parent_admin_user_required
def application_work_experience_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)

    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #     return redirect("application:view_application_twfl", app.slug)

    experience_formset = modelformset_factory(ProfessionalExperience, form=AppWorkExperienceForm, extra=0)
    if request.method == 'POST':
        formset = experience_formset(request.POST, request.FILES)
        form = WouldYouLikeGainAdditionalWorkExperience(request.POST, instance=app)
        if formset.is_valid() and form.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.app = app
                instance.save()
            form.save()
            return redirect('application:application_references_twfl', app.slug)
        else:
            print(formset.errors)
            print(form.errors)
    else:
        form = WouldYouLikeGainAdditionalWorkExperience(instance=app)
        formset = experience_formset(queryset=ProfessionalExperience.objects.filter(app=app.id))
    return render(request, 'application/application_work_experience.html',
                  {'formset': formset, 'form':form, 'app': app})


'''
Date       : 12/23/2020 
Function   : application_references_twfl  
Description: Add references in application form
Parameters : Application ID
Return     : On successful submission redirect to next form  personal statement
'''

@student_parent_admin_user_required
def application_references_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)

    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #     return redirect("application:view_application_twfl", app.slug)

    reference_formset = modelformset_factory(Reference, form=app_references_form, extra=0)
    if request.method == 'POST':
        formset = reference_formset(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.app = app
                instance.save()
            return redirect('application:review_submit_twfl', app.slug)
        else:
            print(formset.errors)
    else:
        formset = reference_formset(queryset=Reference.objects.filter(app=app.id))
    return render(request, 'application/application_references.html',
                  {'formset': formset, 'app': app})


'''
Date       : 12/24/2020 
Function   : application_personal_statement_twfl
Description: Add personal statement in application form 
Parameters : Application ID
Return     : On successful submission redirect to next form - visa history
'''

@student_parent_admin_user_required
def application_personal_statement_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)
    # Application Status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(
    #         app=app.id).first().qualification_achieved is None:
    #     return redirect("application:view_application_twfl", app.slug)
    if PersonalStatement.objects.filter(app=app, institute=None).exists():
        ps_app = PersonalStatement.objects.get(app=app, institute=None)
    else:
        ps_app = PersonalStatement.objects.create(app=app)

    if request.method != "POST":
        form = AppPersonalStatementForm(instance=ps_app)

    else:
        form = AppPersonalStatementForm(request.POST, request.FILES, instance=ps_app)
        if form.is_valid():
            form.save()
            return redirect("application:application_visa_history_twfl", app.slug)
        else:
            print(form.errors)
            messages.error(request, "Failed to save, Form is not valid")
    return render(request, "application/application_personal_statement.html", {'form': form, 'app': app})



@student_parent_admin_user_required
def application_personal_statement_old_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)

    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #     return redirect("application:view_application_twfl", app.slug)

    personal_statement_formset = modelformset_factory(PersonalStatement, form=AppPersonalStatementForm, extra=0)
    # ps_exists = Personal_Statement.objects.filter(app=app).exists()
    ps_exists = PersonalStatement.objects.filter(considered_application__app=app).exists()
    if request.method == 'POST':
        formset = personal_statement_formset(request.POST, request.FILES)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                # instance.app = app
                instance.save()
            return redirect('application:application_visa_history_twfl', app.slug)
        else:
            print(formset.errors)
    else:
        # formset = personal_statement_formset(queryset=Personal_Statement.objects.filter(app=app.id))
        formset = personal_statement_formset(
            queryset=PersonalStatement.objects.filter(considered_application__app=app))
    return render(request, 'application/application_personal_statement_single.html',
                  {'formset': formset, 'app': app, 'ps_exists': ps_exists})


'''
Date       : 12/24/2020 
Function   : application_visa_history_twfl
Description: Add visa history in application form 
Parameters : Application ID
Return     : On successful submission redirect to next form - additional information
'''

@student_parent_admin_user_required
def application_visa_history_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)
    # Application Status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #     return redirect("application:view_application_twfl", app.slug)

    visa_history_Formset = modelformset_factory(VisaHistory, form=AppVisaHistoryForm, extra=0)
    basic_info = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id,
                                                                                   user_slug=request.user.slug)
    passport = AppPassportInformation.objects.using('afm_personal_information').get(app=basic_info)
    passport_form = AppPassportInformationForm(instance=passport)
    if passport.passport:
        passport_form.fields['passport'].widget.attrs.pop('required', None)
    else:
        passport_form.fields['passport'].widget.attrs['required'] = 'required'

    if request.method == 'POST':
        formset_visa_history = visa_history_Formset(request.POST, request.FILES)
        passport_form = AppPassportInformationForm(request.POST, request.FILES, instance=passport)
        if passport.passport:
            passport_form.fields['passport'].widget.attrs.pop('required', None)
        else:
            passport_form.fields['passport'].widget.attrs['required'] = 'required'

        if formset_visa_history.is_valid() and passport_form.is_valid():
            passport_form_obj = passport_form.save(commit=False)
            passport_form_obj.save(using='afm_personal_information')
            instances = formset_visa_history.save(commit=False)
            for instance in instances:
                instance.app = app
                instance.save()
            return redirect('application:application_additional_information_twfl', app.slug)
        else:
            print(formset_visa_history.errors)
    else:
        # messages.error(request, "Failed to save, Form is not valid")
        formset_visa_history = visa_history_Formset(queryset=VisaHistory.objects.filter(app=app.id))
    return render(request, 'application/application_visa_history.html',
                  {'formset': formset_visa_history, 'passport_form': passport_form, 'app': app})


'''
Date       : 12/24/2020 
Function   : application_additional_information_twfl
Description: Add additional information in application form 
Parameters : Application ID
Return     : On successful submission redirect to next form - additional information
'''

@student_parent_admin_user_required
def application_additional_information_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)
    # Application Status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #     return redirect("application:view_application_twfl", app.slug)
    basic_info = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id,
                                                                                   user_slug=request.user.slug)
    if request.method != "POST":
        additional_info_form = AppAdditionalInformationForm(instance=app)
        next_of_kin_form = NextOfKinInformationForm(instance=basic_info)

    else:
        additional_info_form = AppAdditionalInformationForm(request.POST, request.FILES, instance=app)
        next_of_kin_form = NextOfKinInformationForm(request.POST, instance=basic_info)
        if additional_info_form.is_valid() and next_of_kin_form.is_valid():
            additional_info_form.save()
            next_of_kin_form.save()
            return redirect("application:review_submit_twfl", app.slug)

        else:
            print(additional_info_form.errors)
            print(next_of_kin_form.errors)
            messages.error(request, "Failed to save, Form is not valid")
    return render(request, "application/application_additional_information.html",
                          {'additional_info_form': additional_info_form, 'next_of_kin_form':next_of_kin_form, 'app': app})

'''
Function   : review_submit_twfl
Description: Review and submit application form. it will update the application status
Parameters : Application ID
Return     : On successful submission redirect to success page
'''

@student_parent_admin_user_required
def review_submit_twfl(request, app_slug):
    app = Application.objects.get(slug=app_slug, admin=request.user)

    # if app.status in [None, 0, 2] or AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #     return redirect("application:review_submit_twfl", app.slug)

    feedback = ApplicationFeedback.objects.get(app=app)
    basic_info = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id,
                                                                                   user_slug=request.user.slug)
    if request.method != "POST":
        # Get all the application details
        address = AppAddress.objects.using('afm_personal_information').get(app=basic_info)
        passport = AppPassportInformation.objects.using('afm_personal_information').get(app=basic_info)

        educations = AcademicQualification.objects.filter(app=app).order_by('id')
        english_lan = EnglishLanguage.objects.get(app=app)
        experience = ProfessionalExperience.objects.filter(app=app)
        reference = Reference.objects.filter(app=app)
        common_personal_statement = PersonalStatement.objects.filter(app=app)
        personal_statements = PersonalStatement.objects.filter(Q(considered_application__app=app) | Q(app=app))
        visa = VisaHistory.objects.filter(app=app)

        feedback_form = ApplicationFeedbackForm(instance=app)
        mentor_form = SelectMentorForm(instance=app)

        # Look for personal information only if there is any direct application requested
        # if ConsideredApplication.objects.filter(app=app, is_direct_app=True).exists():
        #     if personal_statement[0].question_1 is not None:
        #         is_ps_required = True
        #     else:
        #         is_ps_required = False
        # else:
        #     is_ps_required = True

        # Check if all the forms are filled
        clear = basic_info.about_me is not None
                # and basic_info.marital_status is not None \
                # and educations[0].institute_name is not None
        return render(request, "application/application_review_submit.html",
                      {
                          'consent_additional': app,
                          'direct_applications': ConsideredApplication.objects.filter(app=app, is_direct_app=True),
                          'basic_info': basic_info,
                          'address': address,
                          'passport': passport,
                          'educations': educations,
                          'english_lan': english_lan,
                          'experience': experience,
                          'reference': reference,
                          'common_personal_statement': common_personal_statement.first(),
                          'personal_statements': personal_statements,
                          'visa': visa,
                          'clear': clear,
                          'app': app,
                          'feedback': feedback,
                          'feedback_form': feedback_form,
                          'mentor_form': mentor_form,
                      })
    else:
        # Application Status:
        # (0, 'Approved'),
        # (1, 'Rejected'),
        # (2, 'Completed'),
        # (3, 'Incomplete'),
        app.status = 2
        app.submitted_at = datetime.datetime.now()
        app.consent_terms_condition = True
        app.save()
        # Prepare Notification
        url_name = '#'
        verb = 'Your application is submitted. Now wait for response.'
        notify.send(app.admin,
                    recipient=app.admin,
                    description=url_name,
                    target=app,
                    level='success',
                    verb=verb)
        # url_name = '/application/application/%s' % (app.slug)
        # verb = 'You have been given a feedback by ' + app.admin.first_name + '(' + app.admin.slug + ')' + \
        #        ' for Application submission on ApplyPal'
        # notify.send(app.mentor.admin,
        #             recipient=app.mentor.admin,
        #             description=url_name,
        #             target=app,
        #             level='success',
        #             verb=verb)

        # Send email to application email
        base_link = request.POST.get('link')
        link = f"{base_link}/application/application/{app.slug}"
        # Send email notification
        # send_email_notification.delay('Your application has been submitted successfully',
        #                               'application/application_mail.html',
        #                               [basic_info.email],
        #                               {
        #                                   'user_first_name': app.admin.first_name,
        #                                   'intake_year': app.intake_year,
        #                                   'user_last_name': app.admin.last_name,
        #                                   'applicant_first_name': basic_info.first_name,
        #                                   'link': link,
        #                               }
        #                               )
        # Send email notification to admin
        # Send email to application email
        # send_email_notification.delay('Notification from TAG',
        #                               'application/notification_mail.html',
        #                               [mail_send_from],
        #                               {
        #                                   'link': link,
        #                                   'msg': 'We received a successful application.',
        #                               }
        #                               )
        # Delete all the junk applications
        delete_null_application_instance_twfl(request)
        return redirect("application:application_submitted_first_step_twfl", app.slug)


'''
Function   : application_submitted_twfl
Description: View Submitted Application or redirect to dashboard 
Parameters : Application ID
Return     : --
'''

@student_parent_admin_user_required
def application_submitted_twfl(request, app_slug):
    app = Application.objects.get(admin=request.user, slug=app_slug)
    return render(request, "application/application_submitted.html",
                  {'app': app, })


'''
Author     : Viral Solanki 
Date       : 
Function   : First step of Application form is submitted successfully template
Parameters : Application ID
Return     : --
'''

@student_parent_admin_user_required
def application_submitted_first_step_twfl(request, app_slug):
    app = Application.objects.get(admin=request.user, slug=app_slug)
    form = WouldYouBeInterestedInSharingYourDetailsWithInstitute(instance=app)
    if request.method == 'POST':
        form = WouldYouBeInterestedInSharingYourDetailsWithInstitute(request.POST, instance=app)
        if form.is_valid():
            form.save()
            return cv_pdf(request, app_slug)

    # Check if user has already filled the forms or not by checking form status
    # if AcademicQualification.objects.filter(app=app.id).exists():
    #     if AcademicQualification.objects.filter(app=app.id).first().qualification_achieved is None:
    #         return redirect("application:application_consent_twfl", app.slug)
    return render(request, "application/application_submitted_first_step.html",
                  {'app': app, 'form':form })

'''
Function   : view_application_twfl
Description: View single Application form
Parameters : Application ID
Return     : --
'''

@student_parent_school_admin_user_required
def view_application_twfl(request, app_slug):
    # Check if user is Admin, user type 0 is for super-admin and 1 is for admin
    if request.user.user_type in [0, 1, 11]:
        app = Application.objects.get(slug=app_slug)
    else:
        app = Application.objects.get(slug=app_slug, admin=request.user)
        # Application Status:
        # (0, 'Approved'),
        # (1, 'Rejected'),
        # (2, 'Completed'),
        # (3, 'Incomplete'),
        if app.status is None or AcademicQualification.objects.filter(
                app=app.id).first().qualification_achieved is None:
            return redirect("application:application_consent_twfl", app.slug)
        if app.status in [3, 1]:
            return redirect('application:review_submit_twfl', app_slug)

    app_pi = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id)
    open_comments = ApplicationComment.objects.filter(comment_type=0, app=app).order_by('-created_at')
    temp = []
    for i in app.direct_application.all():
        temp.append(i.institute.id)
    system_mentor = None
    template = "application_view.html"

    # Mark All Notification related to Application as read
    notifications = Notification.objects.filter(target_content_type__model='application', )
    # notifications.mark_all_as_unread()
    additional_questions = None
    if app.admin.user_type == 3:
        additional_questions = AdditionalQuestions.objects.filter(student = app.admin.student)
    return render(request, "application/" + template,
                  {
                      'consent_additional': app,
                      'basic_info': app_pi,
                      'address': app_pi.app_address,
                      'passport': app_pi.app_passport_information,
                      'educations': app.academic_qualifications.all(),
                      'english_lan': app.english_language,
                      'experience': app.professional_experience_app.all(),
                      'reference': app.references_app.all(),
                      'personal_statement': PersonalStatement.objects.filter(Q(considered_application__app=app)|Q(app=app)),
                      'visa': app.visa_history_app.all(),
                      'app': app,
                      'direct_applications': ConsideredApplication.objects.filter(app=app, is_direct_app=True),
                      'institutes_offer': ConsideredApplication.objects.filter(app=app, is_direct_app=False),
                      'personal_statement_form': AppPersonalStatementForm,
                      'app_institute_reject_form': AppInstituteRejectForm,
                      'final_selected': FinalSelected.objects.filter(offer__app=app).first(),
                      'final_selection_dropdown': ConsideredApplication.objects.filter(app=app, offer_status=2),
                      'app_additional_documents_form': AppAdditionalDocumentsForm(),
                      'offer_final_selection_form': OfferFinalSelection(),
                      'offer_final_selection_edit_form': OfferFinalSelection(
                          instance=FinalSelected.objects.filter(offer__app=app).first()),
                      'list_documents': DocumentUpload.objects.filter(app=app),
                      'comment_form': AppCommentForm,
                      'open_comments': open_comments,
                      'system_mentor': system_mentor,
                      'professional_training': ProfessionalTrainingCertificate.objects.filter(app=app),
                      'additional_questions': additional_questions
                  })


'''
Function   : single_application
Description: View single Application form
Parameters : Application ID
Return     : --
'''

@student_parent_admin_user_required
def single_application(request, app, template):
    app_pi = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id)
    open_comments = ApplicationComment.objects.filter(comment_type=0, app=app).order_by('-created_at')
    temp = []
    for i in app.direct_application.all():
        temp.append(i.institute.id)
    system_mentor = None
    if BlockUser.objects.filter(reported_user__slug=app.admin.slug, report_by_user__slug=app.mentor.admin.slug,
                                user_assigned=request.user).exists():
        system_mentor = BlockUser.objects.filter(reported_user__slug=app.admin.slug,
                                                 report_by_user__slug=app.mentor.admin.slug,
                                                 user_assigned=request.user).first()
    elif BlockUser.objects.filter(reported_user__slug=app.mentor.admin.slug, report_by_user__slug=app.admin.slug,
                                  user_assigned=request.user).exists():
        system_mentor = BlockUser.objects.filter(reported_user__slug=app.mentor.admin.slug,
                                                 report_by_user__slug=app.admin.slug,
                                                 user_assigned=request.user).first()
    if system_mentor:
        system_mentor = system_mentor.user_assigned

    return render(request, "application/" + template + '.html',
                  {
                      'consent_additional': app,
                      'basic_info': app_pi,
                      'address': app_pi.app_address,
                      'passport': app_pi.app_passport_information,
                      'educations': app.academic_qualifications.all(),
                      'english_lan': app.english_language,
                      'experience': app.professional_experience_app.all(),
                      'reference': app.references_app.all(),
                      'personal_statement': PersonalStatement.objects.filter(considered_application__app=app),
                      'visa': app.visa_history,
                      'app': app,
                      'direct_applications': ConsideredApplication.objects.filter(app=app, is_direct_app=True),
                      'institutes_offer': ConsideredApplication.objects.filter(app=app, is_direct_app=False),
                      'final_selected': ConsideredApplication.objects.filter(app=app, final_selection=True).first(),
                      'final_selection_dropdown': ConsideredApplication.objects.filter(app=app, offer_status=2),
                      'app_additional_documents_form': AppAdditionalDocumentsForm(),
                      'offer_final_selection_form': OfferFinalSelection(),
                      'list_documents': DocumentUpload.objects.filter(app=app),
                      'comment_form': AppCommentForm,
                      'open_comments': open_comments,
                      'system_mentor': system_mentor,
                  })



@student_user_required
def cv_pdf(request, app_slug, preview=None):
    app = Application.objects.get(slug=app_slug)
    app_pi = AppBasicInformation.objects.using('afm_personal_information').get(app=app.id)
    tag_logo = static('website/img/content-img/Tag.png')
    # tag_logo = request.build_absolute_uri('/static/website/img/content-img/Tag.png')
    print('tag_logo', tag_logo)
    data = {
            'consent_additional': app,
            'basic_info': app_pi,
            'address': app_pi.app_address,
            'passport': app_pi.app_passport_information,
            'educations': app.academic_qualifications.all(),
            'english_lan': app.english_language,
            'experience': app.professional_experience_app.all(),
            'reference': app.references_app.all(),
            'professional_training': ProfessionalTrainingCertificate.objects.filter(app=app),
            'preview': preview,
            'tag_logo':tag_logo,
            }
    if preview:
        return render(request, "application/student_cv.html", data)
    options = {
        'page-size': 'A4',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'encoding': "UTF-8",
        'no-outline': None
    }
    template = get_template("application/student_cv.html")
    html = template.render(data)
    pdf = pdfkit.from_string(html, False, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="' + app_pi.first_name + '-' \
                                      + app_pi.surname +'-cv' + '.pdf"'
    return response


def view_application_mentor_twfl(request, app_id):
    app = Application.objects.get(id=app_id)
    return single_application(request, app, 'student_application')


'''
Function   : application_comments_save_twfl
Description: Put comments on application to interact with AppAdmin
Parameters : Application ID
Return     : Redirect to View application page
'''

@student_parent_admin_user_required
def application_comments_save_twfl(request, app_id):
    app = Application.objects.get(id=app_id)
    if request.method == 'POST':
        form = AppCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.app = app
            instance.app_admin = request.user
            instance.save()
            messages.success(request, "Your response is updated")
            return redirect('application:view_application_twfl', app.slug)
        else:
            messages.error(request, "Failed to save, Form is not valid")
    return redirect("application:view_application_twfl", app.slug)


'''
Function   : comment_reply_twfl
Description: Give reply on comments upto 1 level
Parameters : Parent Comment ID
Return     : Redirect to View application page
'''

@student_parent_admin_user_required
def comment_reply_twfl(request, comment_id):
    parent = ApplicationComment.objects.get(id=comment_id)
    if request.method != 'POST':
        messages.error(request, "Failed to reply, Form is not valid")
    else:
        ApplicationComment.objects.create(comment_type=parent.comment_type, app=parent.app, app_admin=request.user,
                                          comment=request.POST['comment'],
                                          parent=parent)
        messages.success(request, "Your response is updated")
    return redirect("application:view_application_twfl", parent.app.slug)


# -----------------------------------------------------------------------
#     PARENT USER MODULES
# -----------------------------------------------------------------------

'''
Function   : my_applications_twfl
Description: Create multiple application form, list submitted application forms
Parameters : --
Return     : Redirect to My applications page
'''

@parent_admin_user_required
def my_applications_twfl(request):
    # Application Status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    incomplete_app = Application.objects.filter(admin=request.user, status__in=[1, 3], subject=6).count()
    submitted_app = Application.objects.filter(admin=request.user, status__in=[0, 2], subject=6).count()
    if request.method != "POST":
        # Get all Medicine applications, subject code for medicine is 6
        queryset = Application.objects.filter(admin=request.user, subject=6).exclude(status=None).order_by(
            '-created_at')
        filtered_qs = ApplicationFilter(request.GET, queryset)
        if queryset.count() == 0:
            return render(request, "application/no_application.html")
        paginated_filtered = Paginator(filtered_qs.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        return render(request, "application/my_applications.html",
                      {'list_applications': page_obj, 'app': queryset, 'form': filtered_qs.form, 'page_obj': page_obj,
                       'total_app': queryset.count(), 'incomplete_app': incomplete_app, 'submitted_app': submitted_app})

    else:
        app = Application.objects.create(admin=request.user)
        EnglishLanguage.objects.create(app=app)
        VisaHistory.objects.create(app=app)
        Reference.objects.create(app=app)
        ProfessionalExperience.objects.create(app=app)
        ProfessionalTrainingCertificate.objects.create(app=app)
        AcademicQualification.objects.create(app=app)
        ApplicationFeedback.objects.create(app=app)

        # In personal information database
        app_pi = AppBasicInformation.objects.using('afm_personal_information').create(app=app.id,
                                                                                      user_slug=request.user.slug, )
        AppAddress.objects.using('afm_personal_information').create(app=app_pi)
        AppPassportInformation.objects.using('afm_personal_information').create(app=app_pi)
        return redirect('application:application_consent_twfl', app.slug)



'''
Function   : submitted_applications_twfl
Description: List of all the submitted applications
Parameters : --
Return     : Redirect to my application page
'''

@parent_admin_user_required
def submitted_applications_twfl(request):
    # Application Status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    # Get all Medicine applications, subject code for medicine is 6
    incomplete_app = Application.objects.filter(admin=request.user, status__in=[1, 3], subject=6).count()
    total_app = Application.objects.filter(admin=request.user, subject=6).exclude(status=None).count()

    if request.method != "POST":
        if total_app == 0:
            return render(request, "application/no_application.html")

    queryset = Application.objects.filter(admin=request.user, status__in=[0, 2], subject=6)
    filtered_qs = ApplicationFilter(request.GET, queryset)
    paginated_filtered = Paginator(filtered_qs.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginated_filtered.get_page(page_number)

    return render(request, "application/my_applications.html",
                  {'list_applications': page_obj, 'form': filtered_qs.form, 'page_obj': page_obj,
                   'total_app': total_app, 'incomplete_app': incomplete_app, 'submitted_app': queryset.count()})


'''
Function   : incomplete_applications_twfl
Description: List of all the incomplete applications
Parameters : --
Return     : Redirect to my application page
'''

@parent_admin_user_required
def incomplete_applications_twfl(request):
    # Application Status:
    # (0, 'Approved'),
    # (1, 'Rejected'),
    # (2, 'Completed'),
    # (3, 'Incomplete'),
    # Get all Medicine applications, subject code for medicine is 6
    # delete_null_application_instance_twfl(request)
    submitted_app = Application.objects.filter(admin=request.user, status__in=[0, 2], subject=6).count()
    total_app = Application.objects.filter(admin=request.user, subject=6).exclude(status=None).count()
    if request.method != "POST":
        if total_app == 0:
            return render(request, "application/no_application.html")

        queryset = Application.objects.filter(admin=request.user, status__in=[1, 3], subject=6)
        filtered_qs = ApplicationFilter(request.GET, queryset)
        paginated_filtered = Paginator(filtered_qs.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        return render(request, "application/my_applications.html",
                      {'list_applications': page_obj, 'form': filtered_qs.form, 'page_obj': page_obj,
                       'total_app': total_app, 'incomplete_app': queryset.count(), 'submitted_app': submitted_app})


'''
Function   : rejected_applications_twfl
Description: List of all the rejected applications
Parameters : --
Return     : Redirect to my application page
'''

@parent_admin_user_required
def rejected_applications_twfl(request):
    app = Application.objects.filter(admin=request.user).exclude(status=None)
    if request.method != "POST":
        if app.count() == 0:
            return render(request, "application/no_application.html")
        queryset = Application.objects.filter(admin=request.user, status=1, subject=6)
        filtered_qs = ApplicationFilter(request.GET, queryset)
        paginated_filtered = Paginator(filtered_qs.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        return render(request, "application/my_applications.html",
                      {'list_applications': page_obj, 'app': app, 'form': filtered_qs.form, 'page_obj': page_obj})


'''
Function   : approved_applications_twfl
Description: List of all the approved applications
Parameters : --
Return     : Redirect to my application page
'''

@parent_admin_user_required
def approved_applications_twfl(request):
    app = Application.objects.filter(admin=request.user).exclude(status=None)
    if request.method != "POST":
        if app.count() == 0:
            return render(request, "application/no_application.html")
        queryset = Application.objects.filter(admin=request.user, status=0)
        filtered_qs = ApplicationFilter(request.GET, queryset)
        paginated_filtered = Paginator(filtered_qs.qs, 10)
        page_number = request.GET.get('page')
        page_obj = paginated_filtered.get_page(page_number)

        return render(request, "application/my_applications.html",
                      {'list_applications': page_obj, 'app': app, 'form': filtered_qs.form, 'page_obj': page_obj})


'''
Date       : 12/17/2020 
Function   : all_applications_twfl
Description: List available applications
Parameters : --
Return     : Redirect to all applications page
'''

@institute_user_required
def all_applications_twfl(request):
    institute_instance = Institute.objects.get(admin=request.user)
    if institute_instance.account_type:
        total_applications = Application.objects.filter(status=0).exclude(
            exclude_institutes__institute__admin=request.user)
    else:
        total_applications = Application.objects.filter(status=0).exclude(
            exclude_institutes__institute__admin=request.user)[:5]
    return render(request, "institute/list_application.html",
                  {'applications': total_applications})


'''
Date       : 12/17/2020 
Function   : requested_applications_twfl
Description: List direct requested applications for institute
Parameters : --
Return     : Redirect to institute list applications page
'''

@institute_user_required
def requested_applications_twfl(request):
    institute_instance = Institute.objects.get(admin=request.user)
    if institute_instance.account_type:
        requested_applications = institute_instance.selected_institutes.filter(status=0)
    else:
        requested_applications = institute_instance.selected_institutes.filter(status=0)[:5]
    return render(request, "institute/list_application.html",
                  {'applications': requested_applications})


'''
Function   : application_offer_status_by_university
Description: Receive Offer from institute 
Parameters : Application ID
Return     : Redirect to view applications page
'''

@institute_user_required
def application_offer_status_by_university(request, app_id):
    app = Application.objects.get(id=app_id)
    if request.method == 'POST':
        form = AppInstituteFeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.app = app
            instance.institute = request.user
            instance.save()
            messages.success(request, "Your response is updated")
            return redirect('application:view_application_twfl', app.slug)
        else:
            messages.error(request, "Failed to save, Form is not valid")
            return redirect('application:view_application_twfl', app.slug)

    return redirect("application:view_application_twfl", app.slug)


'''
Function   : apply_for_institute_twfl
Description: Select offer from institute 
Parameters : Response ID (Response is offer received from Institute in application_offer_status_by_university)
Return     : Redirect to view applications page
'''

@student_parent_admin_user_required
def apply_for_institute_twfl(request, response_id):
    institute_response = ConsideredApplication.objects.get(id=response_id)
    if request.method != 'POST':
        messages.error(request, "Failed to reply, Form is not valid")
    else:
        # form = AppPersonalStatementForm(request.POST)
        # if form.is_valid():
        institute_response.offer_select = True
        institute_response.offer_select_date = datetime.datetime.now()
        institute_response.save()
        # personal_statement = form.save(commit=False)
        # personal_statement.ConsideredApplication = institute_response
        # personal_statement.save()
        messages.success(request, "Your response is updated")
    return redirect("application:view_application_twfl", institute_response.app.slug)


'''
Function   : apply_for_institute_offer_reject_twfl
Description: Reject offer from institute 
Parameters : Response ID (Response is offer received from Institute in application_offer_status_by_university)
Return     : Redirect to view applications page
'''

@student_parent_admin_user_required
def apply_for_institute_offer_reject_twfl(request, response_id):
    institute_response = ConsideredApplication.objects.get(id=response_id)
    if request.method != 'POST':
        messages.error(request, "Failed to reply, Form is not valid")
    else:
        form = AppInstituteRejectForm(request.POST, instance=institute_response)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.offer_select_date = datetime.datetime.now()
            if form.cleaned_data['offer_reject_reason'] == 'Other':
                instance.offer_reject_reason = form.cleaned_data['specify_offer_reject_reason']
            instance.save()
            messages.success(request, "Your response is updated")
        else:
            messages.error(request, "Invalid form")
    return redirect("application:view_application_twfl", institute_response.app.slug)


'''
Function   : final_section_institute_twfl
Description: Select final offer from institute 
Parameters : final_response_id(Response ID)
Return     : Redirect to view applications page
'''

@student_parent_admin_user_required
def final_section_institute_twfl(request):
    final_response_id = request.POST.get('final_select')
    institute_response = ConsideredApplication.objects.get(id=final_response_id)
    if request.method != 'POST':
        messages.error(request, "Failed to reply, Form is not valid")

    else:
        form = OfferFinalSelection(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.offer = institute_response
            form.save()
            institute_response.final_selection = True
            institute_response.save()
            messages.success(request, "Your response is updated")
        else:
            print(form.errors)
            messages.error(request, "Failed to update your request, try again !")

    return redirect("application:view_application_twfl", institute_response.app.slug)


'''
Function   : final_section_institute_detail_edit_twfl
Description: Edit final offer from institute 
Parameters : final_response_id(Response ID)
Return     : Redirect to view applications page
'''

@student_parent_admin_user_required
def final_section_institute_detail_edit_twfl(request, form_id):
    final_section_institute_detail = FinalSelected.objects.get(id=form_id)
    if request.method != 'POST':
        messages.error(request, "Failed to reply, Form is not valid")

    else:
        form = OfferFinalSelection(request.POST, request.FILES, instance=final_section_institute_detail)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.approve_status = None
            instance.save()
            messages.success(request, "Your response is updated")
        else:
            print(form.errors)
            messages.error(request, "Failed to update your request, try again !")

    return redirect("application:view_application_twfl", final_section_institute_detail.offer.app.slug)

'''
Function   : application_additional_document_twfl
Description: Add additional documents in your application form in case it is require
Parameters : Application ID
Return     : Redirect to view applications page
'''

@student_parent_admin_user_required
def application_additional_document_twfl(request, app_id):
    app = Application.objects.get(id=app_id)
    if request.method != "POST":
        return redirect("application:view_application_twfl", app.slug)
    else:
        app_form = AppAdditionalDocumentsForm(request.POST, request.FILES)
        if app_form.is_valid():
            doc = app_form.save(commit=False)
            doc.app = app
            doc.admin = request.user
            doc.save()
            messages.success(request, "Your document is uploaded successfully")

            return redirect("application:view_application_twfl", app.slug)

        else:
            print(app_form.errors)
            messages.error(request, "Failed to upload document, try again !")
            return redirect("application:view_application_twfl", app.slug)


'''
Function   : application_delete_additional_document_twfl
Description: Delete additional documents in your application form in case it is require
Parameters : Application ID
Return     : Redirect to view applications page
'''

@student_parent_admin_user_required
def application_delete_additional_document_twfl(request, id):
    document_instance = DocumentUpload.objects.get(id=id)
    if request.method == "POST":
        document_instance.delete()
    return redirect("application:view_application_twfl", document_instance.app.slug)


def get_institute(request):
    if request.method == 'GET':
        country = request.GET['country']
        if request.GET['app']:
            app = request.GET['app']
            changeConfirmation = request.GET['changeConfirmation']
            app = get_object_or_404(Application, id=app)
            if changeConfirmation:
                app.study_destination_country = country
                app.save()
            trash = ConsideredApplication.objects.filter(app=app)
            if trash:
                for instance in trash:
                    instance.delete()
        country = Institute.objects.filter(country=country).order_by('institute_name')

        return JsonResponse({"country": serialize('json', queryset=country)}, status=200)


def get_institute_consent(request):
    if request.method == 'GET':
        country_json = request.GET['country']
        country = json.loads(country_json)
        if request.GET['app']:
            app = request.GET['app']
            # trash = considered_application.objects.filter(app=app)
            # if trash:
            #     for instance in trash:
            #         instance.delete()
        country = Institute.objects.filter(country__in=country).order_by('institute_name')
        return JsonResponse({"country": serialize('json', queryset=country)}, status=200)


def get_passport_exists(request):
    if request.method == 'GET':
        passport_exist = False
        passport = request.GET['passport']
        app_id = request.GET['app_id']
        if AppPassportInformation.objects.filter(passport_number=passport).exclude(app=app_id).exists():
            passport_exist = True

        return JsonResponse({"passport_exist": passport_exist})


def clear_direct_application(request):
    if request.method == 'GET':
        is_cleared = False
        instance = request.GET['instance']
        if ConsideredApplication.objects.filter(id=instance).exists():
            ConsideredApplication.objects.get(id=instance).delete()
            is_cleared = True

        return JsonResponse({"is_cleared": is_cleared})


def add_considered_application_field_value(request):
    instances = PersonalStatement.objects.all()
    for instance in instances:

        if instance.app and instance.institute:
            ca_instance = ConsideredApplication.objects.get(app=instance.app, institute=instance.institute)
            if ca_instance:
                if not instance.ConsideredApplication:
                    instance.ConsideredApplication = ca_instance
                    instance.save()
    messages.success(request, "Updated Successfully")
    return redirect("/")


@super_admin_user_required
def fill_application_form_permission_twfl(request, app_slug):
    app = get_object_or_404(Application, slug=app_slug)
    if app.fill_form_permission:
        app.fill_form_permission = False
        messages.success(request, "Access Revoked")
        app.save()
    else:
        app.fill_form_permission = True
        app.save()
        # Send email to application email
        link = ''.join(
            [config('AFM_LINK'), '/application/application/', str(app.slug)])

        send_email_notification.delay('Notification from ApplyPal',
                                      'application/notification_mail.html',
                                      [app.admin.email],
                                      {
                                          'link': link,
                                          'msg': 'Your application request is approved. Please complete '
                                                 'your rest of the form.',
                                      }
                                      )
        messages.success(request, "Access Approved.")
    return redirect('application:view_application_twfl', app_slug)

