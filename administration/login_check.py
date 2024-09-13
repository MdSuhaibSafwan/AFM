from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from administration.models import Mentor
from personal_information.models import StudentPersonalInformation


def check_if_student_completed_profile(user):
    if user.user_type == 3:
        pi_user = StudentPersonalInformation.objects.using('afm_personal_information').get(
            admin__user_slug=user.slug)
        if pi_user.admin.gender or pi_user.admin.gender == 0:
            return True
        else:
            return False
    return True


def check_if_mentor_has_approved_profile(user):
    if user.user_type == 4:
        mentor_profile = Mentor.objects.get(admin=user)
        if mentor_profile.profile_status:
            return True
        else:
            return False
    return True


def check_if_applicant_is_not_applying_for_EU_countries(user):
    show = False
    if user.user_type == 3:
        applicant_pi = get_object_or_404(StudentPersonalInformation, admin__user_slug=user.slug)
        EU_countries = ['GB', 'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT',
                        'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']
        if applicant_pi.admin.currently_living_in in EU_countries:
            if 'GB' in applicant_pi.study_destination:
                show = True
    return show

def check_if_student_has_application_fill_permission(user):
    show = True
    if user.user_type in [3, 5]:
        if user.application.all().first().academic_qualifications.all().first().country:
            show = True
        else:
            show = False
    return show


super_admin_login_required = user_passes_test(lambda user: user.user_type == 0, login_url='/404/')
admin_login_required = user_passes_test(lambda user: user.user_type == 1 or user.user_type == 0, login_url='/404/')
institute_login_required = user_passes_test(lambda user: user.user_type == 2 or user.user_type == 0, login_url='/404/')
student_login_required = user_passes_test(lambda user: user.user_type == 3 or user.user_type == 0, login_url='/404/')
student_complete_profile_required = user_passes_test(check_if_student_completed_profile, login_url='/update-profile/')
applicant_is_not_applying_for_EU_countries = user_passes_test(check_if_applicant_is_not_applying_for_EU_countries,
                                                              login_url='/update-profile/')
student_has_application_fill_permission = user_passes_test(check_if_student_has_application_fill_permission,
                                                              login_url='/404/')
mentor_login_required = user_passes_test(lambda user: user.user_type == 4 or user.user_type == 0, login_url='/404/')
mentor_has_approved_profile = user_passes_test(check_if_mentor_has_approved_profile,
                                                              login_url='/404/')
parent_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 0, login_url='/404/')
student_parent_institute_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 0 or user.user_type == 2, login_url='/404/')
student_parent_mentor_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 4 or user.user_type == 0,
    login_url='/404/')


def admin_user_required(view_func):
    decorated_view_func = login_required(admin_login_required(view_func), login_url='login')
    return decorated_view_func


def student_user_required(view_func):
    decorated_view_func = login_required(student_login_required(view_func), login_url='login')
    return decorated_view_func


def student_user_complete_profile_required(view_func):
    decorated_view_func = login_required(student_complete_profile_required(view_func), login_url='login')
    return decorated_view_func


# def student_user_complete_profile_required(view_func):
#     decorated_view_func = login_required(applicant_is_not_applying_for_EU_countries(view_func), login_url='login')
#     return decorated_view_func


def parent_admin_user_required(view_func):
    decorated_view_func = login_required(parent_login_required(view_func), login_url='login')
    return decorated_view_func


def student_parent_admin_user_required(view_func):
    decorated_view_func = login_required(student_parent_institute_login_required(view_func), login_url='login')
    return decorated_view_func


def student_parent_mentor_admin_user_required(view_func):
    decorated_view_func = login_required(student_parent_mentor_login_required(view_func), login_url='login')
    return decorated_view_func


def institute_user_required(view_func):
    decorated_view_func = login_required(institute_login_required(view_func), login_url='login')
    return decorated_view_func


def mentor_user_required(view_func):
    decorated_view_func = login_required(mentor_login_required(view_func), login_url='login')
    return decorated_view_func


def super_admin_user_required(view_func):
    decorated_view_func = login_required(super_admin_login_required(view_func), login_url='login')
    return decorated_view_func

def student_has_application_fill_permission_required(view_func):
    decorated_view_func = login_required(student_has_application_fill_permission(view_func), login_url='login')
    return decorated_view_func