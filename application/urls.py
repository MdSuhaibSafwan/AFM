from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView

app_name = 'application'
urlpatterns = [
    # ----------------------------- STUDENT MODULE------------------------------
    path('my-applications/',            views.my_applications_twfl,                  name='my_applications_twfl'),
    path('submitted-applications/',     views.submitted_applications_twfl,           name='submitted_applications_twfl'),
    path('incomplete-applications/',    views.incomplete_applications_twfl,          name='incomplete_applications_twfl'),
    path('rejected-applications/',      views.rejected_applications_twfl,            name='rejected_applications_twfl'),
    # ----------------------------- APPLICATION FORMS ------------------------------
    path('start/<str:app_slug>/',         views.application_consent_twfl,              name='application_consent_twfl'),
    path('personal-information/<str:app_slug>/',
                                        views.application_personal_information_twfl,
                                                                                     name='application_personal_information_twfl'),
    path('get-passport-exists/',        views.get_passport_exists,                   name='get-passport-exists'),
    path('education/<str:app_slug>/',     views.application_education_twfl,            name='application_education_twfl'),
    path('training-certification/<str:app_slug>/',
                                        views.application_training_twfl,             name='application_training_twfl'),
    path('english-language/<str:app_slug>/',
                                        views.application_english_language_twfl,     name='application_english_language_twfl'),
    path('work-experience/<str:app_slug>/',views.application_work_experience_twfl,     name='application_work_experience_twfl'),
    path('reference/<str:app_slug>/',     views.application_references_twfl,           name='application_references_twfl'),
    path('personal-statement/<str:app_slug>/',
                                        views.application_personal_statement_twfl,   name='application_personal_statement_twfl'),
    path('visa-history/<str:app_slug>/',  views.application_visa_history_twfl,         name='application_visa_history_twfl'),
    path('additional-information/<str:app_slug>/',
                                        views.application_additional_information_twfl,name='application_additional_information_twfl'),
    path('review/<str:app_slug>/',        views.review_submit_twfl,                    name='review_submit_twfl'),
    path('application/<str:app_slug>/',   views.view_application_twfl,                 name='view_application_twfl'),
    path('application-initial-status/<str:app_slug>/',
                                        views.application_submitted_first_step_twfl, name='application_submitted_first_step_twfl'),
    path('application-status/<str:app_slug>/',
                                        views.application_submitted_twfl,            name='application_submitted_twfl'),

    path('application_comments_save_twfl/<str:app_id>/',
                                        views.application_comments_save_twfl,        name='application_comments_save_twfl'),

    path('application_additional_document_twfl/<str:app_id>/',
                                        views.application_additional_document_twfl,  name='application_additional_document_twfl'),

    path('comment_reply_twfl/<str:comment_id>/',
                                        views.comment_reply_twfl,                    name='comment_reply_twfl'),

    path('apply_for_institute_twfl/<str:response_id>/',
                                        views.apply_for_institute_twfl,              name='apply_for_institute_twfl'),
    path('apply_for_institute_offer_reject_twfl/<str:response_id>/',
                                        views.apply_for_institute_offer_reject_twfl, name='apply_for_institute_offer_reject_twfl'),

    path('final_section_institute_twfl/',views.final_section_institute_twfl,         name='final_section_institute_twfl'),

    path('final_section_institute_detail_edit_twfl/<str:form_id>/',
                                        views.final_section_institute_detail_edit_twfl,
                                                                                     name='final_section_institute_detail_edit_twfl'),

    path('get-institute/',             views.get_institute,                         name='get-institute'),
    path('get-institute-consent/',     views.get_institute_consent,                 name='get_institute_consent'),
    path('clear-direct-application/',  views.clear_direct_application,              name='clear_direct_application'),
    # ----------------------------- MENTOR MODULE------------------------------

    path('view-application-mentor/<str:app_id>/',
                                        views.view_application_mentor_twfl,          name='view_application_mentor_twfl'),

    # ----------------------------- PARENT MODULE------------------------------

    path('my-applications/',            views.my_applications_twfl,                  name='my_applications_twfl'),

    # ----------------------------- ADMIN MODULE------------------------------
    path('application-delete-additional-document/<int:id>',
        views.application_delete_additional_document_twfl,       name='application_delete_additional_document_twfl'),
    path('fill-application-form-permission/<str:app_slug>/', views.fill_application_form_permission_twfl, name='fill_application_form_permission_twfl'),

    # ----------------------------- INSTITUTE MODULE------------------------------
    path('requested_applications/',     views.requested_applications_twfl,           name='requested_applications_twfl'),
    path('approved_applications/',      views.approved_applications_twfl,            name='approved_applications_twfl'),
    path('all-applications/',           views.all_applications_twfl,                 name='all_applications_twfl'),
    path('application_offer_status_by_university/<str:app_id>/',
                                        views.application_offer_status_by_university,  name='application_offer_status_by_university'),
    path('add-considered-application-field-value/',
                                        views.add_considered_application_field_value,        name='add_considered_application_field_value'),
    path('cv-pdf/<str:app_slug>/<str:preview>', views.cv_pdf, name='cv_pdf'),
    path('cv-pdf/<str:app_slug>/', views.cv_pdf, name='cv_pdf'),


]
