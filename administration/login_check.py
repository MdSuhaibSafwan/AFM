from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from administration.models import Mentor
from personal_information.models import StudentPersonalInformation
from AFM.settings import SPECIAL_MENTOR_SLUG


def check_if_student_completed_profile(user):
    if user.user_type == 3:
        pi_user = StudentPersonalInformation.objects.using('afm_personal_information').get(
            admin__user_slug=user.slug)
        if pi_user.admin.gender or pi_user.admin.gender == 0:
            return True
        else:
            return False
    return True


def check_if_special_mentor_profile(user):
    if user.user_type == 4:
        if user.slug == SPECIAL_MENTOR_SLUG:
            return True
        else:
            return False
    return False


def check_if_future_student_or_special_mentor_profile(user):
    if user.user_type == 4:
        if user.slug == SPECIAL_MENTOR_SLUG:
            return True
        else:
            return False
    if user.user_type == 12:
        return True
    return False


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
special_mentor_required = user_passes_test(check_if_special_mentor_profile, login_url='/404/')
future_student_special_mentor_login_required = user_passes_test(check_if_future_student_or_special_mentor_profile,
                                                                login_url='/404/')
applicant_is_not_applying_for_EU_countries = user_passes_test(check_if_applicant_is_not_applying_for_EU_countries,
                                                              login_url='/update-profile/')
student_has_application_fill_permission = user_passes_test(check_if_student_has_application_fill_permission,
                                                           login_url='/404/')
mentor_login_required = user_passes_test(lambda user: user.user_type == 4 or user.user_type == 0, login_url='/404/')
mentor_has_approved_profile = user_passes_test(check_if_mentor_has_approved_profile,
                                               login_url='/404/')
parent_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 0, login_url='/404/')
future_student_login_required = user_passes_test(
    lambda user: user.user_type == 12 or user.user_type == 0, login_url='/404/')
student_parent_institute_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 0 or user.user_type == 2,
    login_url='/404/')
student_future_student_parent_institute_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 12 or user.user_type == 0 or
                 user.user_type == 2, login_url='/404/')
student_parent_school_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 0 or user.user_type == 11,
    login_url='/404/')
student_future_student_parent_school_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 0 or user.user_type == 12 or
                 user.user_type == 11, login_url='/404/')
student_parent_mentor_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 4 or user.user_type == 0,
    login_url='/404/')
student_future_mentor_login_required = user_passes_test(
    lambda user: user.user_type == 12 or user.user_type == 4 or user.user_type == 0,
    login_url='/404/')
student_future_student_parent_mentor_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 4 or user.user_type == 0 or
                 user.user_type == 4 or user.user_type == 12,
    login_url='/404/')
student_parent_mentor_school_login_required = user_passes_test(
    lambda
        user: user.user_type == 5 or user.user_type == 3 or user.user_type == 4 or user.user_type == 0 or user.user_type == 11,
    login_url='/404/')
future_student_student_parent_mentor_school_login_required = user_passes_test(
    lambda user: user.user_type == 5 or user.user_type == 3 or user.user_type == 4 or user.user_type == 0 or
                 user.user_type == 11 or user.user_type == 12,
    login_url='/404/')
school_login_required = user_passes_test(
    lambda user: user.user_type == 11 or user.user_type == 0, login_url='/404/')


def admin_user_required(view_func):
    decorated_view_func = login_required(admin_login_required(view_func), login_url='login')
    return decorated_view_func


def student_user_required(view_func):
    decorated_view_func = login_required(student_login_required(view_func), login_url='login')
    return decorated_view_func


def student_user_complete_profile_required(view_func):
    decorated_view_func = login_required(student_complete_profile_required(view_func), login_url='login')
    return decorated_view_func


def special_mentor_user_required(view_func):
    decorated_view_func = login_required(special_mentor_required(view_func), login_url='login')
    return decorated_view_func


# def student_user_complete_profile_required(view_func):
#     decorated_view_func = login_required(applicant_is_not_applying_for_EU_countries(view_func), login_url='login')
#     return decorated_view_func


def parent_admin_user_required(view_func):
    decorated_view_func = login_required(parent_login_required(view_func), login_url='login')
    return decorated_view_func


def future_student_admin_user_required(view_func):
    decorated_view_func = login_required(future_student_login_required(view_func), login_url='login')
    return decorated_view_func


def future_student_special_mentor_user_required(view_func):
    decorated_view_func = login_required(future_student_special_mentor_login_required(view_func), login_url='login')
    return decorated_view_func


def student_parent_admin_user_required(view_func):
    decorated_view_func = login_required(student_parent_institute_login_required(view_func), login_url='login')
    return decorated_view_func


def student_future_student_parent_admin_user_required(view_func):
    decorated_view_func = login_required(student_future_student_parent_institute_login_required(view_func),
                                         login_url='login')
    return decorated_view_func


def student_parent_school_admin_user_required(view_func):
    decorated_view_func = login_required(student_parent_school_login_required(view_func), login_url='login')
    return decorated_view_func


def student_future_student_parent_school_admin_user_required(view_func):
    decorated_view_func = login_required(student_future_student_parent_school_login_required(view_func),
                                         login_url='login')
    return decorated_view_func


def student_parent_mentor_admin_user_required(view_func):
    decorated_view_func = login_required(student_parent_mentor_login_required(view_func), login_url='login')
    return decorated_view_func


def student_future_mentor_admin_user_required(view_func):
    decorated_view_func = login_required(student_future_mentor_login_required(view_func), login_url='login')
    return decorated_view_func


def student_future_student_parent_mentor_admin_user_required(view_func):
    decorated_view_func = login_required(student_future_student_parent_mentor_login_required(view_func),
                                         login_url='login')
    return decorated_view_func


def student_parent_mentor_school_admin_user_required(view_func):
    decorated_view_func = login_required(student_parent_mentor_school_login_required(view_func), login_url='login')
    return decorated_view_func


def future_student_student_parent_mentor_school_admin_user_required(view_func):
    decorated_view_func = login_required(future_student_student_parent_mentor_school_login_required(view_func),
                                         login_url='login')
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


def school_admin_user_required(view_func):
    decorated_view_func = login_required(school_login_required(view_func), login_url='login')
    return decorated_view_func
