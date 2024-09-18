from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from administration.api import DemandAndSupply
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from administration.login_check import super_admin_user_required

app_name = 'administration'

urlpatterns = [
    path('',  views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.registration, name='registration'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('select-user/', views.select_user_type, name='select_user_type'),
    path('404/', views.page_not_found, name='page_not_found'),
    
    path('former-student/registration/', views.former_student_registration, name='former_student_registration'),
    path('current-student/registration/', views.current_student_registration, name='current_student_registration'),
  
    # path('clear_url_slug/', views.clear_url_slug, name='clear_url_slug'),
    path('mentor-booking-list/', super_admin_user_required(views.MentorBookingLeadsList.as_view()), name='mentor_booking_list'),
    path('mentor-booking-leads/<str:slug>/', views.mentor_booking_leads, name='mentor_booking_leads'),
    path('demand-and-supply/', views.demand_n_supply, name='demand_n_suppy'),
    path('demand-and-supply-data-list/', super_admin_user_required(views.DemandAndSupplyList.as_view()), name='dns_list'),
    path('api/get-demand-n-supply/', login_required(DemandAndSupply.as_view()), name='demand_n_suppy_api'),
    # path('chat/login/', views.chat_login, name='chat-login'),
    path('chat/ajax/google-slug-session/', views.ajax_google_slug_session, name='ajax_google_slug_session'),

    #  added by areeb
    path('pk/', views.home_pk, name='home_pk'), # Added By Areeb
    path('ind/', views.home_ind, name='home_ind'), # Added By Areeb
    path('plan/study-university-abroad/', views.planner, name='planner'), # Added By Areeb
    
    path('connect-with-your-peers/terms-and-conditions/', views.terms_and_conditions, name='terms-and-conditions'),
    path('study-abroad/privacy-notice/', views.privacy_notice, name='privacy-notice'),
    path('universities-abroad/cookies-policy/', views.cookies_policy, name='cookies-policy'),
    path('tutor-for-university/safeguarding/', views.safeguarding, name='safeguarding'),
    path('peer-to-peer-tutoring/online-safety/', views.online_safety, name='online-safety'),
    path('tutors-students-mentors/codes-of-conduct/', views.codes_of_conduct, name='codes-of-conduct'),

    # path('get-phone-number/', views.get_phone_number, name='get_phone_number'),
    
    path('register-now-to-start-medical-school-abroad/', views.redirect_registration, name='redirect_registration'),
    path('register/<str:mentor_slug>/', views.registration, name='registration'),
    path('get-email-exists/', views.get_email_exists, name='get-email-exists'),
    path('get-email-exists-on-afu/', views.get_email_exists_on_afu, name='get-email-exists-on-afu'),
    # path('register-as-an-alumnus/', views.mentor_registration, name='mentor_registration'),
    
    # ----------------------------Alumni Profile-------------------------- #
    path('update-profile/', views.update_profile_twfl, name='update_profile_twfl'),
    path('update-profile/<str:mentor_slug>/', views.update_profile_twfl, name='update_profile_twfl'),
    path('update-profile-step-1/', views.upload_public_information_twfl, name='upload_public_information_twfl'),
    path('update-profile-step-2/', views.upload_private_information_twfl, name='upload_private_information_twfl'),
    path('update-profile-step-3/', views.upload_profile_photo_and_consent_twfl, name='upload_profile_photo_and_consent_twfl'),

    
    # ----------------------------Current Students Profile-------------------------- #  
    path('current-student-profile-step-1/', views.current_student_profile_step_1, name='current_student_profile_step_1'), #new
    path('current-student-profile-step-2/', views.current_student_profile_step_2, name='current_student_profile_step_2'), #new
    path('current-student-profile-step-3/', views.current_student_profile_step_3, name='current_student_profile_step_3'), #new
    
    path('thanking/', views.thanking, name='thanking'), #new
    
    path('confirmAccount/<str:slug>/', views.confirmAccount),
    path('confirmAccount/<str:slug>/<str:mentor_slug>', views.confirmAccount),
    path('change-password/', views.change_password, name='change_password'),
    path('check-username-password/', views.check_username_password, name='check-username-password'),
    path('check-profile-password/', views.check_profile_password, name='check-profile-password'),
    path('update-profile-pic/<int:pk>/', views.update_profile_pic, name='update_profile_pic'),  # arc4.21feb2
    path('delete-profile-pic/<str:slug>/', views.delete_profile_pic, name='delete_profile_pic'),
    path('user-registration/', views.user_registration, name='user_registration'),
    
    
    # **************** STUDENT MODULES *****************
    path('search-alumni/', views.search_mentors_twfl, name='search_mentors_twfl'),
    path('new-search-all/', views.new_search_all, name='new_search_all'),
    path('new-search-alumni/', views.new_search_alumni, name='new_search_alumni'),
    path('new-search-students/', views.new_search_students, name='new_search_students'),
    path('search-students/', views.search_students_twfl, name='search_students_twfl'),
    path('ajax-loggeduser-status/<str:slug>/', views.ajax_loggeduser_status, name='ajax_loggeduser_status'),
    path('sample-mentor-profile/',
             TemplateView.as_view(template_name='administration/sample_mentor_profile.html'),
             name='sample_mentor_profile'),
    
    path('student_profile_step_1/', views.student_profile_step_1, name='student_profile_step_1'),
    path('student_profile_step_2/', views.student_profile_step_2, name='student_profile_step_2'),
    path('student-profile/<str:slug>/', views.student_profile_twfl, name='student_profile'),


    # path('alumni/public-profile1/study-<slug:currently_studying_slug>/<slug:name_slug>-from-<slug:country_slug>/',
    #     views.alumni_public_profile1, name='alumni_public_profile1'),

    # path('student/public-profile/<int:area_of_study>/<slug:name_slug>-from-<slug:country_slug>/',
    #     views.student_public_profile, name='student_public_profile'),
    
    path('alumni/public-profile/study-<slug:currently_studying_slug>/<slug:name_slug>-from-<slug:country_slug>/',
        views.alumni_public_profile, name='alumni_public_profile'),

    path('ifg/student/public-profile/<slug:user_slug>/',
        views.ifg_student_public_profile, name='ifg_student_public_profile'),

    path(
        'uk-medical-schools/study-<slug:currently_studying_slug>-at-<slug:institute_in>/<slug:name_slug>-from-<slug:country_slug>/',
        views.student_single_mentor_twfl, name='student_single_mentor_twfl'),
    path(
        'uk-medical-schools/study-<slug:currently_studying_slug>-at-<slug:institute_in>/<slug:name_slug>-from-<slug:country_slug>/<slug:url_slug>/',
        views.student_single_mentor_using_url_slug_twfl, name='student_single_mentor_using_url_slug_twfl'),
    # path(
    #     'uk-medical-schools/study-<slug:currently_studying_slug>-at-<slug:institute_in>/<slug:name_slug>-from-<slug:country_slug>/<str:slug>/',
    #     views.student_single_mentor_using_slug_twfl, name='student_single_mentor_using_slug_twfl'),
    path('mentor-subscribe/', views.mentor_subscribe_twfl, name='mentor_subscribe_twfl'),
    path('default-search/<str:user_slug>/', views.default_search_twfl, name='default_search_twfl'),
    # **************** ADMIN MODULES *****************
    path('list-alumni/', views.list_mentors_twfl, name='list_mentors_twfl'),
    path('mentor-latepoint-link/<str:id>/', views.MentorLatepointLink, name='mentor_latepoint_link'),
    path('admin-meeting-link/', views.admin_meeting_link, name='admin_meeting_link'),
    path('app-admins/', views.list_app_admin_twfl, name='list_app_admin_twfl'),
    path('recruiters/', views.list_recruiters_twfl, name='list_recruiters_twfl'),
    path('institute-lead/', views.list_lead_institute_twfl, name='list_lead_institute_twfl'),
    path('tech-support-enquires/', views.list_tech_support_twfl, name='list_tech_support_twfl'),
    path('contact-enquires/', views.list_contact_leads_twfl, name='list_contact_leads_twfl'),
    path('change-status-is-active/<str:admin_id>/',
         views.change_status_is_active_twfl, name='change_status_is_active_twfl'),
    path('change-testimonials-status-is-active/<str:id>/',
         views.change_testimonials_status_is_active_twfl, name='change_testimonials_status_is_active_twfl'),
    
    path('approve-alumni/<str:admin_slug>/', views.approve_mentor_twfl, name='approve_mentor_twfl'),
    path('approve-student/<str:admin_slug>/', views.approve_student_twfl, name='approve_student_twfl'),

    path('create-unique-url-slug/<str:admin_slug>/', views.create_unique_url_slug_for_mentor_twfl, name='create_unique_url_slug_for_mentor_twfl'),
    path('list-mentor-testimonials/', views.list_mentor_testimonials, name='list_mentor_testimonials'),
    path('list-system-mentor/', views.list_system_mentors_twfl, name='list_system_mentors_twfl'),
    path('list-system-recruiter/', views.list_system_recruiter_twfl, name='list_system_recruiter_twfl'),
    path('list-future-students/', views.list_future_students_twfl, name='list_future_students_twfl'),
    path('system-mentor-registration/', views.system_mentor_registration_twfl, name='system_mentor_registration_twfl'),
    path('recruiter-registration/', views.recruiter_registration_twfl, name='recruiter_registration_twfl'),
    path('system-recruiter-registration/', views.system_recruiter_registration_twfl,
         name='system_recruiter_registration_twfl'),
    path('delete-user/<str:user_slug>/', views.delete_user_twfl, name='delete_user_twfl'),
    path('mentor-profile-about-me-field-update/<str:slug>/', views.mentor_update_about_me_field_twfl,
         name='mentor_update_about_me_field_twfl'),
    path('mentor-profile-youtube-shots-field-update/<str:slug>/', views.mentor_update_youtube_shots_field_twfl,
         name='mentor_update_youtube_shots_field_twfl'),
    path('import-user/', views.import_user_twfl, name='import_user_twfl'),
    path('import/', views.import_data, name='import_data'),

    # **************** PARENT MODULES *****************
    path('update-profile-parent/', views.update_parent_profile_twfl, name='update_parent_profile_twfl'),
    path('update-profile-parent/<str:mentor_slug>/', views.update_parent_profile_twfl, name='update_parent_profile_twfl'),
    path('my-parent-profile/<str:slug>/', views.parent_profile_twfl, name='parent_profile_twfl'),
    
    # **************** MENTOR MODULES *****************
    path('list-students/', views.list_students_twfl, name='list_students_twfl'),
    path('list-parents/', views.list_parents_twfl, name='list_parents_twfl'),
    path('recruiters/', views.list_recruiters_twfl, name='list_recruiters_twfl'),
    path('user-applications/<str:user_slug>/',
         views.view_applications_of_user_twfl, name='view_applications_of_user_twfl'),
    path('list-mentor-profile-links/',
         views.test_link_list_mentors_twfl, name='test_link_list_mentors_twfl'),

    # **************** APP ADMIN *****************
    path('app-admin-registration/', views.app_admin_registration, name='app_admin_registration'),

    # **************** Institute *****************
    path('institute_admin_registration/', views.institute_admin_registration_twfl,
         name='institute_admin_registration_twfl'),
    path('institute-mentors/', views.institute_mentors_twfl, name='institute_mentors_twfl'),

    path('how-it-work/', views.how_it_work_twfl, name='how_it_work_twfl'),
    path('tech-support/', views.tech_support_twfl, name='tech_support_twfl'),
    path('student-profile/<str:slug>/', views.student_profile, name='student_profile'),
    path('alumni-profile/<str:slug>/', views.mentor_profile_twfl, name='mentor_profile'),
    path('institute/', views.list_institutes_twfl, name='list_institutes_twfl'),
    path('institute-registration/', views.institute_registration_twfl, name='institute_registration_twfl'),
    path('institute-details/<str:slug>/', login_required(views.InstituteDetails.as_view()), name='institute_information'),
    path('update-institute-detail/<int:pk>/', views.institute_update, name='institute_information_edit'),
    path('delete-profile-pic/<int:id>/', views.delete_institute_profile_pic, name='delete_institute_profile_pic'),
    path('update-institute-logo/<int:pk>/', views.update_profile_pic_institute, name='update_profile_pic_institute'),
    path('delete-institute/<int:pk>/', super_admin_user_required(views.InstituteDelete.as_view()), name='delete_institute'),
    path('contact/', views.contact_us_twfl, name='contact_us'),
    # path('message-mentor/<str:user_slug>', views.message_mentor_twfl, name='message_mentor_twfl'),

    # **************** Website static pages *****************

    # path('parents/',
    #      TemplateView.as_view(template_name='website/parents.html'),
    #      name='parents'),
    #
    # path('university-contact/', views.university_contact_form,
    #      name='university_contact_form'),
    # path('study-medicine/',
    #      TemplateView.as_view(template_name='website/study-medicine.html'),
    #      name='study_medicine'),
    #
    # path('uk-medical-schools/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/index.html'),
    #      name='uk_medical_schools'),
    #
    # path('uk-medical-schools/widening-access/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/widening-access.html'),
    #      name='widening_access'),
    #
    # path('uk-medical-schools/studying-medicine-at-anglia-ruskin-university/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-anglia-ruskin-university.html'),
    #      name='studying_medicine_at_anglia_ruskin_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-aston-university/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-aston-university.html'),
    #      name='studying_medicine_at_aston_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-barts/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-barts.html'),
    #      name='studying_medicine_at_barts'),
    #
    # path('uk-medical-schools/studying-medicine-at-brighton-and-sussex-medical-school/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-brighton-and-sussex-medical-school.html'),
    #      name='studying_medicine_at_brighton_and_sussex_medical_school'),
    #
    # path('uk-medical-schools/studying-medicine-at-brunel-university-london/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-brunel-university-london.html'),
    #      name='studying_medicine_at_brunel_university_london'),
    #
    # path('uk-medical-schools/studying-medicine-at-newcastle-university/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-newcastle-university.html'),
    #      name='studying_medicine_at_newcastle_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-exeter/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-exeter.html'),
    #      name='studying_medicine_at_the_university_of_exeter'),
    #
    # path('uk-medical-schools/studying-medicine-at-norwich-medical-school/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-norwich-medical-school.html'),
    #      name='studying_medicine_at_norwich_medical_school'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-glasgow/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-glasgow.html'),
    #      name='studying_medicine_at_the_university_of_glasgow'),
    #
    # path('uk-medical-schools/studying-medicine-at-anglia-ruskin-university/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-anglia-ruskin-university.html'),
    #      name='studying_medicine_at_anglia_ruskin_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-peninsula-medical/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-peninsula-medical.html'),
    #      name='studying_medicine_at_peninsula_medical'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-leeds/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-leeds.html'),
    #      name='studying_medicine_at_the_university_of_leeds'),
    #
    # path('uk-medical-schools/studying-medicine-at-aston-university/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-aston-university.html'),
    #      name='studying_medicine_at_aston_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-queens-university/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-queens-university.html'),
    #      name='studying_medicine_at_queens_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-leicester/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-leicester.html'),
    #      name='studying_medicine_at_the_university_of_leicester'),
    #
    # path('uk-medical-schools/studying-medicine-at-barts/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-barts.html'),
    #      name='studying_medicine_at_barts'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-lincoln/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-lincoln.html'),
    #      name='studying_medicine_at_the_university_of_lincoln'),
    #
    # path('uk-medical-schools/studying-medicine-at-brighton-and-sussex-medical-school/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-brighton-and-sussex-medical-school.html'),
    #      name='studying_medicine_at_brighton_and_sussex_medical_school'),
    #
    # path('uk-medical-schools/studying-medicine-at-st-georges-university-of-london/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-st-georges-university-of-london.html'),
    #      name='studying_medicine_at_st_georges_university_of_london'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-liverpool/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-liverpool.html'),
    #      name='studying_medicine_at_the_university_of_liverpool'),
    #
    # path('uk-medical-schools/studying-medicine-at-swansea-university/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-swansea-university.html'),
    #      name='studying_medicine_at_swansea_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-nottingham/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-nottingham.html'),
    #      name='studying_medicine_at_the_university_of_nottingham'),
    #
    # path('uk-medical-schools/studying-medicine-at-cardiff-university/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-cardiff-university.html'),
    #      name='studying_medicine_at_cardiff_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-college-london-ucl/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-college-london-ucl.html'),
    #      name='studying_medicine_at_the_university_college_london_ucl'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-oxford/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-oxford.html'),
    #      name='studying_medicine_at_the_university_of_oxford'),
    #
    # path('uk-medical-schools/studying-medicine-at-edge-hill-university/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-edge-hill-university.html'),
    #      name='studying_medicine_at_edge_hill_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-aberdeen-school-of-medicine/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-aberdeen-school-of-medicine.html'),
    #      name='studying_medicine_at_the_university_of_aberdeen_school_of_medicine'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-sheffield/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-sheffield.html'),
    #      name='studying_medicine_at_the_university_of_sheffield'),
    #
    # path('uk-medical-schools/studying-medicine-at-hull-york-medical-school/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-hull-york-medical-school.html'),
    #      name='studying_medicine_at_hull_york_medical_school'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-birmingham/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-birmingham.html'),
    #      name='studying_medicine_at_the_university_of_birmingham'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-southampton/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-southampton.html'),
    #      name='studying_medicine_at_the_university_of_southampton'),
    #
    # path('uk-medical-schools/studying-medicine-at-imperial-college-london/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-imperial-college-london.html'),
    #      name='studying_medicine_at_imperial_college_london'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-bristol/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-bristol.html'),
    #      name='studying_medicine_at_the_university_of_bristol'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-st-andrews/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-st-andrews.html'),
    #      name='studying_medicine_at_the_university_of_st_andrews'),
    #
    # path('uk-medical-schools/studying-medicine-at-keele-university/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-keele-university.html'),
    #      name='studying_medicine_at_keele_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-buckingham/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-buckingham.html'),
    #      name='studying_medicine_at_the_university_of_buckingham'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-sunderland/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-sunderland.html'),
    #      name='studying_medicine_at_the_university_of_sunderlandol'),
    #
    # path('uk-medical-schools/studying-medicine-at-kent-and-medway-medical-school/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-kent-and-medway-medical-school.html'),
    #      name='studying_medicine_at_kent_and_medway_medical_school'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-cambridge/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-cambridge.html'),
    #      name='studying_medicine_at_the_university_of_cambridge'),
    #
    # path('uk-medical-schools/studying-medicine-at-ulster-university/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-ulster-university.html'),
    #      name='studying_medicine_at_ulster_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-kings-college-london-kcl/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-kings-college-london-kcl.html'),
    #      name='studying_medicine_at_kings_college_london_kcl'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-central-lancashire-uclan/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-central-lancashire-uclan.html'),
    #      name='studying_medicine_at_the_university_of_central_lancashire_uclan'),
    #
    # path('uk-medical-schools/studying-medicine-at-warwick/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-warwick.html'),
    #      name='studying_medicine_at_warwick'),
    #
    # path('uk-medical-schools/studying-medicine-at-lancaster-university/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-lancaster-university.html'),
    #      name='studying_medicine_at_lancaster_university'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-dundee/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-dundee.html'),
    #      name='studying_medicine_at_the_university_of_dundee'),
    #
    # path('uk-medical-schools/studying-medicine-at-manchester/',
    #      TemplateView.as_view(template_name='website/uk-medical-schools/studying-medicine-at-manchester.html'),
    #      name='studying_medicine_at_manchester'),
    #
    # path('uk-medical-schools/studying-medicine-at-the-university-of-edinburgh/',
    #      TemplateView.as_view(
    #          template_name='website/uk-medical-schools/studying-medicine-at-the-university-of-edinburgh.html'),
    #      name='studying_medicine_at_the_university_of_edinburgh'),
    #
    # path('graduate-entry-to-medicine/',
    #      TemplateView.as_view(template_name='website/graduate-entry-to-medicine.html'),
    #      name='graduate_entry_to_medicine'),
    #
    # path('uk-medical-school-admissions-tests/',
    #      TemplateView.as_view(template_name='website/uk-medical-school-admissions-tests.html'),
    #      name='medical_school_admissions_tests'),
    #
    # path('medical-school-mentor/',
    #      TemplateView.as_view(template_name='website/medical-school-mentor.html'),
    #      name='medical_school_mentor'),
    #
    # path('study-medicine-in-australia/',
    #      TemplateView.as_view(template_name='website/study-medicine-in-australia/index.html'),
    #      name='study_medicine_in_australia'),
    #
    # path('study-medicine-in-ireland/',
    #      TemplateView.as_view(template_name='website/study-medicine-in-ireland/index.html'),
    #      name='study_medicine_in_ireland'),
    #
    # path('study-medicine-in-the-caribbean/', views.study_medicine_in_the_caribbean_twfl,
    #      name='study_medicine_in_the_caribbean'),
    #
    # path('study-medicine-in-canada/',
    #      TemplateView.as_view(template_name='website/study-medicine-in-canada/index.html'),
    #      name='study_medicine_in_canada'),
    #
    # path('study-medicine-in-the-usa/',
    #      TemplateView.as_view(template_name='website/study-medicine-in-the-usa/index.html'),
    #      name='study_medicine_in_the_usa'),
    #
    # path('medical-schools-in-europe/', views.medical_schools_in_europe_twfl,
    #      name='study_medicine_in_europe'),
    #
    # path('medical-schools-in-europe/studying-medicine-at-karolinska-institute/',
    #      TemplateView.as_view(
    #          template_name='website/medical-schools-in-europe/studying-medicine-at-karolinska-institute.html'),
    #      name='studying_medicine_at_karolinska_institute'),
    #
    # path('medical-schools-in-europe/studying-medicine-at-charles-university/',
    #      TemplateView.as_view(
    #          template_name='website/medical-schools-in-europe/studying-medicine-at-charles-university.html'),
    #      name='studying_medicine_at_charles_university'),
    #
    # path('medical-schools-in-europe/studying-medicine-at-medical-university-sofia/',
    #      TemplateView.as_view(
    #          template_name='website/medical-schools-in-europe/studying-medicine-at-medical-university-sofia.html'),
    #      name='studying_medicine_at_medical_university_sofia'),
    #
    # path('medical-schools-in-europe/studying-medicine-at-the-medical-university-of-silesia/',
    #      TemplateView.as_view(
    #          template_name='website/medical-schools-in-europe/studying-medicine-at-the-medical-university-of-silesia.html'),
    #      name='studying_medicine_at_the_medical_university_of_silesia'),
    #
    # path('study-medicine-in-ireland/studying-medicine-at-national-university-of-ireland/',
    #      TemplateView.as_view(
    #          template_name='website/study-medicine-in-ireland/studying-medicine-at-national-university-of-ireland.html'),
    #      name='studying_medicine_at_national_university_of_ireland'),
    #
    # path('study-medicine-in-ireland/studying-medicine-at-royal-college-of-surgeons/',
    #      TemplateView.as_view(
    #          template_name='website/study-medicine-in-ireland/studying-medicine-at-royal-college-of-surgeons.html'),
    #      name='studying_medicine_at_royal_college_of_surgeons'),
    #
    # path('study-medicine-in-ireland/studying-medicine-at-trinity-college-dublin/',
    #      TemplateView.as_view(
    #          template_name='website/study-medicine-in-ireland/studying-medicine-at-trinity-college-dublin.html'),
    #      name='studying_medicine_at_trinity_college_dublin'),
    #
    # path('study-medicine-in-ireland/studying-medicine-at-university-college-cork-ucc/',
    #      TemplateView.as_view(
    #          template_name='website/study-medicine-in-ireland/studying-medicine-at-university-college-cork-ucc.html'),
    #      name='studying_medicine_at_university_college_cork_ucc'),
    #
    # path('study-medicine-in-ireland/studying-medicine-at-university-college-dublin/',
    #      TemplateView.as_view(
    #          template_name='website/study-medicine-in-ireland/studying-medicine-at-university-college-dublin.html'),
    #      name='studying_medicine_at_university_college_dublin'),
    #
    # path('study-medicine-in-ireland/studying-medicine-at-university-of-limerick/',
    #      TemplateView.as_view(
    #          template_name='website/study-medicine-in-ireland/studying-medicine-at-university-of-limerick.html'),
    #      name='studying_medicine_at_university_of_limerick'),
    #
    path('email-template/',
             TemplateView.as_view(
                 template_name='email/mentor_booking_leads.html'),
             name='email-template'),
    #
    # path('robots.txt',
    #      TemplateView.as_view(
    #          template_name='robots.txt', content_type='text/plan'),
    #      name='robots-txt'),

    # path('sitemap.xml',
    #          TemplateView.as_view(
    #              template_name='sitemap.xml',
    #              content_type='text/xml')),

    # path('test-web-notification/', views.test_web_notification,
    #      name='test_web_notification'),

    # Redirection
    # path('blogs/medical-school-application/medicine-is-personal/', views.redirect_blog_url, name='redirect_blog_url'),


    path('terms-and-conditions/',TemplateView.as_view(template_name='terms-and-condition.html'),
        name='terms_and_conditions'),

    path('privacy-notice/',TemplateView.as_view(template_name='privacy-notice.html'),
        name='privacy_notice'),

    path('cookies-policy/',TemplateView.as_view(template_name='cookies-policy.html'),name='cookies_policy'),

    path('safeguarding-policy/',TemplateView.as_view(template_name='safeguarding-policy.html'),
        name='safeguarding_policy'),

    path('online-safety/',TemplateView.as_view(
            template_name='online-safety.html'),
        name='online_safety'),

    path('codes-of-conduct/',TemplateView.as_view(
            template_name='codes-of-conduct.html'),
        name='codes_of_conduct'),

    path('student-data-clone/', views.clone_data_of_student_table, name="clone_data_of_student_table"),
    path('mobile-data-clone/', views.clone_data_of_mobile_field, name="clone_data_of_mobile_field"),

]
