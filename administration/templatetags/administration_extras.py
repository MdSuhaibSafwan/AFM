import os
import re
import datetime
from django import template
from django.contrib.sites.shortcuts import get_current_site
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from application.models import ApplicationLog, Application, ConsideredApplication, PersonalStatement, VisaHistory, \
    AcademicQualification, EnglishLanguage
from django.shortcuts import get_object_or_404
from messaging.models import Messaging, ReportUser
from personal_information.models import AppBasicInformation, MentorPersonalInformation, \
    StudentPersonalInformation, CustomUserPersonalInformation
from administration.models import CustomUser, Student, Parent, Mentor, Institute, Subscriber, MentorPublicProfileComment
from AFM.utils import get_current_request
from decouple import config
from django.db.models import Q
from django.templatetags.static import static
from django.core.files.storage import default_storage
from django.conf import settings

register = template.Library()


@register.filter
def getmonth(value):
    if value == 0:
        return 'January'
    if value == 1:
        return 'February'
    if value == 2:
        return 'March'
    if value == 3:
        return 'April'
    if value == 4:
        return 'May'
    if value == 5:
        return 'June'
    if value == 6:
        return 'July'
    if value == 7:
        return 'August'
    if value == 8:
        return 'September'
    if value == 9:
        return 'October'
    if value == 10:
        return 'November'
    if value == 11:
        return 'December'
    else:
        return '--'


@register.filter
def getstatus(value):
    if value == 0:
        return 'Approved'
    if value == 1:
        return 'Rejected'
    if value == 2:
        return 'Completed'
    if value == 3:
        return 'Incomplete'
    else:
        return '--'


@register.filter
def getsubject(value):
    if value == 1:
        return 'Business Studies'
    if value == 2:
        return 'Social Studies'
    if value == 3:
        return 'Arts & Design'
    if value == 4:
        return 'Law'
    if value == 5:
        return 'Biomedical Sciences'
    if value == 6:
        return 'Medicine'
    if value == 7:
        return 'Dentistry'
    if value == 8:
        return 'pharmacy'
    if value == 9:
        return 'Computer Science'
    if value == 10:
        return 'Finance'
    if value == 11:
        return 'Architecture'
    if value == 12:
        return 'Finance & Accounting'
    if value == 13:
        return 'Nursing'
    if value == 14:
        return 'Politics'
    if value == 15:
        return 'Chemical Engineering'
    if value == 16:
        return 'Electrical Engineering'
    if value == 17:
        return 'International Relations'
    if value == 18:
        return 'Mechanical Engineering'
    if value == 19:
        return 'Economics'
    if value == 20:
        return 'Civil Engineering'
    else:
        return '--'


@register.filter
def getpost(value):
    if value == 0:
        return 'Foundation'
    if value == 1:
        return 'Undergraduate'
    if value == 2:
        return 'Postgraduate'
    if value == 3:
        return 'Research'
    else:
        return '--'


@register.filter
def getprogramme_level(value):
    if value == 0:
        return 'Foundation'
    if value == 1:
        return 'Undergraduate'
    if value == 2:
        return 'Postgraduate'
    if value == 3:
        return 'Research'
    else:
        return '--'
    # if value == 0:
    #     return 'SSC'
    # if value == 1:
    #     return 'HSC'
    # if value == 2:
    #     return 'A Level'
    # if value == 3:
    #     return 'GCSE'
    # if value == 4:
    #     return 'Bachelors'
    # if value == 5:
    #     return 'Masters'
    # if value == 6:
    #     return 'PhD'
    # if value == 7:
    #     return 'Diploma'
    # if value == 8:
    #     return 'International Year'
    # if value == 9:
    #     return 'Associate Degree'
    # if value == 10:
    #     return 'Professional Certificate'


@register.filter
def getprogramme_level_mentor(value):
    if value == 0:
        return 'Foundation'
    if value == 1:
        return 'Undergraduate'
    if value == 2:
        return 'Postgraduate'
    if value == 3:
        return 'Research'
    else:
        return '--'


@register.filter
def getlang(value):
    if value == 'english':
        return 'English'
    if value == 'hindi':
        return 'Hindi'
    if value == 'gujarati':
        return 'Gujarati'
    else:
        return '--'


@register.filter
def getgender(value):
    if value == 0:
        return 'Male'
    if value == 1:
        return 'Female'
    if value == 2:
        return 'Prefer not to say'
    else:
        return '--'


@register.filter
def gettuttiontype(value):
    if value == 0:
        return 'Privately'
    if value == 1:
        return 'Online Platform'
    else:
        return '--'


@register.filter
def getenglish_level(value):
    if value == 0:
        return 'Beginners'
    if value == 1:
        return 'Elementary'
    if value == 2:
        return 'Intermediate'
    if value == 3:
        return 'Advanced'
    if value == 4:
        return 'Native Speaker'
    else:
        return '--'
    # if value == 0:
    #     return 'Beginner'
    # if value == 1:
    #     return 'Elementary'
    # if value == 2:
    #     return 'Pre-intermediate'
    # if value == 3:
    #     return 'Low Intermediate'
    # if value == 4:
    #     return 'Intermediate'
    # if value == 5:
    #     return 'Upper Intermediate'
    # if value == 6:
    #     return 'Pre-advanced'
    # if value == 7:
    #     return 'Advanced'
    # if value == 8:
    #     return 'Very Advanced'


@register.filter
def getuser(value):
    if value == 0:
        return 'TAG Admin'
    if value == 1:
        return 'Admin'
    if value == 2:
        return 'Institute'
    if value == 3:
        return 'Student'
    if value == 4:
        return 'Alumni'
    if value == 5:
        return 'Parent'
    if value == 6:
        return 'Institute admin'
    if value == 7:
        return 'App admin'
    if value == 8:
        return 'Recruiter'
    if value == 9:
        return 'System Mentor'
    if value == 10:
        return 'System Recruiter'
    if value == 11:
        return 'School'
    if value == 12:
        return 'Future Student'


@register.filter
def getiamachoice(value):
    if value == 1:
        return 'Student'
    if value == 2:
        return 'Parent'
    if value == 3:
        return 'Mentor'
    if value == 4:
        return 'University'
    if value == 5:
        return 'Collage'
    else:
        return '--'


@register.filter
def getfullname(value):
    instance = AppBasicInformation.objects.using('afm_personal_information').get(app=value)
    fullname = instance.title + ' ' if instance.title else '--'
    fullname += instance.first_name + ' ' if instance.first_name else ''
    fullname += instance.surname if instance.surname else ''
    return fullname


@register.filter
def getprofilepicture(value):
    profile_pic = static('images/default_profile.png')
    user_instance = CustomUser.objects.get(slug=value)
    if user_instance.user_type in [4]:
        personal_information_instance = CustomUserPersonalInformation.objects.using('afm_personal_information').get(
            user_slug=value)
        if personal_information_instance.profile_pic:
            profile_pic = personal_information_instance.profile_pic.url
    else:
        if user_instance.profile_pic:
            profile_pic = user_instance.profile_pic.url
    return profile_pic


@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)

    return url


@register.filter
def list2str(x):
    if x:
        x = x[1:][:-1]
        x = x.replace("','", '-')
        x = x[1:][:-1]
        return x


@register.filter
def print_languages(x):
    if x:
        str = ''
        for i in x:
            str = str + i.language + ', '
        return str[:-2]
    return '--'


@register.filter
def print_study_destination(x):
    if x:
        str = ''
        for i in x:
            if i.name:
                str = str + i.name + ', '
        return str[:-2]
    return '--'


@register.filter
def getfilename(value):
    try:
        return os.path.basename(value.file.name)
    except:
        return 'Document'


@register.filter
def getcountry(value):
    instance = AppBasicInformation.objects.using('afm_personal_information').get(app=value)
    print(instance.nationality)
    return instance.nationality.name


@register.filter
def getcountryflag(value):
    instance = AppBasicInformation.objects.using('afm_personal_information').filter(app=value).first()
    nationality = ''
    if instance:
        nationality = instance.nationality.flag
    return nationality


@register.filter
def getfinalselectiontime(value):
    print(value)
    instance = ApplicationLog.objects.filter(app__id=value, type=10).first()
    print(instance)
    return instance.created_at


@register.filter
def getmarital(value):
    if value == '0':
        return 'Single'
    if value == '1':
        return 'Married'
    else:
        return '--'


@register.filter
def getstudyyear(value):
    if value == 1:
        return 'First Year'
    if value == 2:
        return 'Second Year'
    if value == 3:
        return 'Third Year'
    if value == 4:
        return 'Fourth Year'
    if value == 5:
        return 'Fifth Year'
    if value == 6:
        return 'Sixth Year'


@register.filter
def getyesnostatus(value):
    if value == 0:
        return 'No'
    elif value == 1:
        return 'Yes'
    elif value == True:
        return 'Yes'
    elif value == False:
        return 'No'
    else:
        return '--'


@register.filter
def gethealthstatus(value):
    if value == '0':
        return 'No'
    if value == '1':
        return 'Yes'


@register.filter
def getstudystatus(value):
    if value == 1:
        return 'Yes'
    if value == 0:
        return 'No'


@register.filter
def getifappsubmitted(value):
    if Application.objects.filter(admin__id=value, status__in=[0, 1, 2]).first():
        return True
    else:
        return False


@register.filter
def getifselecteduser(value):
    mentor = get_object_or_404(Mentor, admin__slug=value)

    request = get_current_request()
    user = request.user
    if not user.is_authenticated:
        return False

    print(value)
    if user.user_type == 3:
        student = get_object_or_404(Student, admin=user)
        if mentor in student.mentor.all():
            return True
        else:
            return False
    elif user.user_type == 5:
        parent = get_object_or_404(Parent, admin=user)
        if mentor in parent.mentor.all():
            return True
        else:
            return False
    else:
        return False


@register.filter
def getfeedback(value):
    if value == '0':
        return 'Poor'
    if value == '1':
        return 'Satisfactory'
    if value == '2':
        return 'Good'
    if value == '3':
        return 'Very Good'
    if value == '4':
        return 'Excellent'


@register.filter
def getinstitute(value):
    # direct_app = get_object_or_404(considered_application, id=value)
    personal_statement = PersonalStatement.objects.filter(id=value).first()
    if personal_statement.considered_application:
        return personal_statement.considered_application.institute.institute_name
    else:
        return '--'


@register.filter
def getvisahistorycountry(value):
    visa_history = VisaHistory.objects.filter(id=value).first()
    if visa_history:
        return getifneedtheartical(
            visa_history.study_destination_country.code) + visa_history.study_destination_country.name
    else:
        return '--'


@register.filter
def getifmentees(value):
    user_mentor = Mentor.objects.get(admin__id=value)
    students = user_mentor.student_set.all()
    if students:
        return True
    return False


@register.filter
def getpoststatus(value):
    if value == 0:
        return 'Draft'
    if value == 1:
        return 'Submitted for Review'
    if value == 2:
        return 'Published'


@register.filter
def getifnone(value):
    if value:
        return value
    else:
        return '--'


@register.filter
def getdocumenttype(value):
    if value == 1:
        return 'Conditional Offer'
    if value == 2:
        return 'Unconditional Offer'
    if value == 3:
        return 'CAS Letter'
    if value == 4:
        return 'Application Unsuccessful'
    if value == 5:
        return 'Qualification'
    if value == 6:
        return 'English Language'
    if value == 7:
        return 'Training'
    if value == 8:
        return 'Personal Statement'
    if value == 9:
        return 'Resume/CV'
    if value == 10:
        return 'Portfolio'
    if value == 11:
        return 'Research Proposal'
    if value == 12:
        return 'Passport/Visa Document'
    if value == 13:
        return 'Invoice'
    if value == 14:
        return 'Proof of Payment'
    if value == None:
        return 'Additional Document'


@register.filter
def getrecruitertype(value):
    if value == 1:
        return 'Institute'
    if value == 2:
        return 'Recruiter'
    if value == 3:
        return 'School'


@register.filter
def getifneedtheartical(value):
    if value in ['BS', 'KY', 'TC', 'GB', 'AE', 'UM', 'US', 'VG', 'VI', 'NL']:
        return ' the '
    else:
        return ''


@register.filter
def geturlform(value):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", '', s)

    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", '-', s)


@register.simple_tag
def getlatestqualification(id, value):
    latest_qualification = AcademicQualification.objects.filter(app__id=id).order_by(
        '-course_duration_to_year').order_by('-course_duration_to_month').first()
    if latest_qualification:
        if value == 'qualification':
            text = "<div class='col-lg-4'><p class='p-tag'><strong>"
            text += "Currently Studying: " if latest_qualification.is_currently_studying == 1 else "Qualification Achieved: "
            text += "</strong></p></div>"
            text += "<div class='col-lg-8'><p><span>" + getifnone(
                latest_qualification.qualification_achieved) + "</span></p></div>"
            return mark_safe(text)
        if value == 'grade':
            text = "<div class='col-lg-4'><p class='p-tag'><strong>"
            text += "Grades Predicted: " if latest_qualification.is_currently_studying == 1 else "Grades Achieved: "
            text += "</strong></p></div>"
            text += "<div class='col-lg-8'><p><span>" + getifnone(
                latest_qualification.grades_achieved) + "</span></p></div>"
            return mark_safe(text)
        if value == 'country':
            text = "<div class='col-lg-4'><p class='p-tag'><strong>Country Studied: </strong></p></div>"
            text += "<div class='col-lg-8'><p><span>"
            text += getifnone(latest_qualification.country.name) + "<img src=" + getifnone(
                latest_qualification.country.flag) + "alt='flag'>" if latest_qualification.is_currently_studying == 1 else "--"
            text += "</span></p></div>"
            return mark_safe(text)
    else:
        return '--'


@register.simple_tag
def getenglishlanguagescore(id, value):
    latest_qualification = EnglishLanguage.objects.get(app__id=id)
    if latest_qualification:
        if value == 'certificate_name':
            return getifnone(latest_qualification.certificate_name)
        if value == 'overall':
            return getifnone(latest_qualification.overall)
        if value == 'listening':
            return getifnone(latest_qualification.listening)
        if value == 'reading':
            return getifnone(latest_qualification.reading)
        if value == 'speaking':
            return getifnone(latest_qualification.speaking)
        if value == 'writing':
            return getifnone(latest_qualification.writing)
    else:
        return '--'


@register.filter
def getmentorinstituteslug(value):
    user_mentor = get_object_or_404(Mentor, id=value)
    if user_mentor.institute:
        return user_mentor.institute.institute_slug
    else:
        return user_mentor.institute_name_slug


@register.filter
def getifoneormorementor(value):
    user_mentor_pi = get_object_or_404(MentorPersonalInformation, admin__user_slug=value)
    instances = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        admin__name_slug=user_mentor_pi.admin.name_slug, currently_studying_slug=user_mentor_pi.currently_studying_slug,
        admin__country_slug=user_mentor_pi.admin.country_slug)
    if instances.count() > 1:
        return False
    else:
        return True


@register.filter
def getbirthdomain(value):
    request = get_current_request()
    print('Current Domain', get_current_site(request).domain)
    if value == 6:
        # return 'http://' + get_current_site(request).domain + '/uk-medical-schools'
        return config('AFM_LINK') + '/uk-medical-schools'
    else:
        return config('AFM_LINK') + '/university-application-mentors'


# @register.filter
# def getmentorprofileurl(value):
#     user_mentor_pi = get_object_or_404(MentorPersonalInformation, admin__user_slug=value)
#     user_mentor = get_object_or_404(Mentor, admin__slug=value)
#     instances = MentorPersonalInformation.objects.using('afm_personal_information').filter(
#         admin__name_slug=user_mentor_pi.admin.name_slug,
#         currently_studying_slug=user_mentor_pi.currently_studying_slug,
#         admin__country_slug=user_mentor_pi.admin.country_slug)
#     link = ''.join([getbirthdomain(user_mentor_pi.currently_studying), '/study-',
#                     user_mentor_pi.currently_studying_slug, '-at-', getmentorinstituteslug(user_mentor.id), '/',
#                     user_mentor_pi.admin.name_slug, '-from-', user_mentor_pi.admin.country_slug])
#     if instances.count() > 1:
#         return link + '/' + user_mentor.admin.slug
#     else:
#         return link

@register.filter
def getmentorprofileurl(value, with_birth_domain=True):
    user_mentor_pi = get_object_or_404(MentorPersonalInformation, admin__user_slug=value)
    user_mentor = get_object_or_404(Mentor, admin__slug=value)
    instances = MentorPersonalInformation.objects.using('afm_personal_information').filter(
        admin__name_slug=user_mentor_pi.admin.name_slug,
        currently_studying_slug=user_mentor_pi.currently_studying_slug,
        admin__country_slug=user_mentor_pi.admin.country_slug)
    if with_birth_domain:
        link = ''.join([getbirthdomain(user_mentor_pi.currently_studying), '/study-',
                        user_mentor_pi.currently_studying_slug, '-at-', getmentorinstituteslug(user_mentor.id), '/',
                        user_mentor_pi.admin.name_slug, '-from-', user_mentor_pi.admin.country_slug, '/'])
    else:
        link = ''.join(['/uk-medical-schools/study-',
                        user_mentor_pi.currently_studying_slug, '-at-', getmentorinstituteslug(user_mentor.id), '/',
                        user_mentor_pi.admin.name_slug, '-from-', user_mentor_pi.admin.country_slug, '/'])
    if user_mentor_pi.url_slug:
        return link + str(user_mentor_pi.url_slug) + '/'
    return link


@register.filter
def getsubscriberscount(value):
    subscribers = Subscriber.objects.filter(subscribe_to__admin__slug=value)
    return subscribers.count()


@register.filter
def getsubscribers(value):
    subscribers = Subscriber.objects.filter(subscribe_to__admin__slug=value)
    return subscribers


@register.filter
def gettotalsubmittedapplication(value):
    applications = Application.objects.filter(admin__id=value, status__in=[0, 1, 2, 3]).count()
    return applications


@register.filter
def gettotalrequestedapplication(value):
    applications = Application.objects.filter(admin__id=value, status__in=[3], fill_form_permission=False).count()
    return applications


@register.filter
def getschoolurl(value):
    if value == 'GB':
        url = '/uk-medical-schools/'
        string = 'UK Medical Schools'
    elif value == 'IE':
        url = '/study-medicine-in-ireland/'
        string = 'Medical Schools In Ireland'
    elif value == 'US':
        url = '/study-medicine-in-the-usa/'
        string = 'Study medicine in the USA'
    elif value == 'CA':
        url = '/study-medicine-in-canada/'
        string = 'Study medicine in Canada'
    elif value == 'AU':
        url = '/study-medicine-in-australia/'
        string = 'Study medicine in Australia'
    # Countries in Europe
    elif value in ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI',
                   'FR', 'DE', 'GR', 'HU', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL',
                   'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'AL', 'AD', 'AM', 'BY',
                   'BA', 'FO', 'GE', 'GI', 'IS', 'IM', 'XK', 'LI', 'MK', 'MD', 'MC',
                   'ME', 'NO', 'RU', 'SM', 'RS', 'CH', 'TR', 'UA', 'VA']:
        url = '/medical-schools-in-europe/'
        string = 'Medical Schools In Europe'
    else:
        url = '/medical-school-mentor/'
        string = 'Mentors'
    url = "<a href='" + url + "'>" + string + "</a>"
    return mark_safe(url)


@register.simple_tag(takes_context=True)
def live_unread_comments(context, badge_class='live_unread_comments'):
    request = get_current_request()
    user = request.user
    if not user:
        return ''
    # if MessageModel.objects.filter(user=user, read=False).count():
    #     return ''
    reported_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                               is_removed=False).values_list('reported_user')
    # Exclude users from which current user get reported from
    reported_by_users = ReportUser.objects.filter(Q(report_by_user=request.user) | Q(reported_user=request.user),
                                                  is_removed=False).values_list('report_by_user')
    unread_msg = Messaging.objects.filter(receiver=request.user,
                                          read=False).exclude(Q(sender=request.user) | Q(sender__in=reported_by_users)
                                                              | Q(sender__in=reported_users)).count()
    # unread_msg = Messaging.objects.filter(receiver=user, read=False).exclude(
    #     sender=request.user).count()
    if unread_msg > 0:
        html = "<span class='{badge_class}' >{unread}</span>".format(
            badge_class=badge_class, unread=unread_msg
        )
    else:
        html = "<span class='{badge_class}' style='display: none;'>{unread}</span>".format(
            badge_class=badge_class, unread=unread_msg
        )
    return format_html(html)


@register.filter
def get_user_live_unread_comments_count(value):
    request = get_current_request()
    user = request.user
    if not user:
        return ''
    unread_msg = MentorPublicProfileComment.objects.filter(sender__slug=value,
                                                           receiver=request.user,
                                                           read=False).exclude(sender=request.user).count()
    if unread_msg > 0:
        html = "<span class='unread_msgs' user_slug='{user_slug}' >{unread}</span>".format(user_slug=value,
                                                                                           unread=unread_msg
                                                                                           )
    else:
        html = "<span class='unread_msgs' user_slug='{user_slug}' style='display: none;'>{unread}</span>".format(
            user_slug=value,
            unread=unread_msg
        )
    return format_html(html)


@register.filter
def getmessagedate(id):
    msg_object = MentorPublicProfileComment.objects.get(id=id)
    if MentorPublicProfileComment.objects.filter(created_at__year=msg_object.created_at.year,
                                                 created_at__month=msg_object.created_at.month,
                                                 created_at__day=msg_object.created_at.day,
                                                 sender__in=[msg_object.sender, msg_object.receiver],
                                                 receiver__in=[msg_object.sender, msg_object.receiver]).order_by(
        'created_at').first().id == id:
        delta = datetime.date.today() - msg_object.created_at.date()
        if delta.days == 0:
            days_to_go = 'Today'
        elif delta.days == 1:
            days_to_go = 'A day ago'
        else:
            days_to_go = str(delta.days) + " days ago"
        html = "<label class='az-chat-time'><span>{date}</span></label>".format(date=days_to_go)
        return format_html(html)
    return ''


@register.filter
def get_if_applicant_is_not_applying_for_EU_countries(value):
    applicant_pi = get_object_or_404(StudentPersonalInformation, admin__user_slug=value)
    EU_countries = ['GB', 'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT',
                    'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']
    show = False
    if applicant_pi.admin.currently_living_in in EU_countries:
        if 'GB' in applicant_pi.study_destination:
            show = True
    return show


@register.filter
def get_type(value):
    return type(value)


@register.filter
def print_values(list):
    return (", ".join(list))


@register.filter
def get_if_user_from_EU_countries(value):
    user_pi = get_object_or_404(CustomUserPersonalInformation, user_slug=value)
    EU_countries = ['GB', 'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT',
                    'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']
    show = False
    if user_pi.country in EU_countries:
        show = True
    return show

@register.filter
def check_if_file_exists(value=None):
    if value is None:
        return False

    # Get the absolute path of the file in the static directory
    try:
        image_file_path = os.path.join(settings.STATIC_ROOT, value)
    except TypeError as e:
        print(e)
        return False
    
    print("Value - ", value)
    print('image_file_path ', image_file_path, os.path.exists(image_file_path))

    # Check if the file path exists
    if os.path.exists(image_file_path):
        # File exists, return a success response or perform further actions
        return True
    else:
        # File doesn't exist, return a not found response or handle the case
        return False
