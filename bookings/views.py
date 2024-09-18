import json

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import *
from bookings.models import Services, Appointment, Timeslots, AppointmentCancelRequests
from administration.models import CustomUser, Mentor, School, Student
from django.core.mail import send_mail
from payments.models import *
from personal_information.models import StudentPersonalInformation
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages
import pytz
from .helpers import time_tz_conversion, get_user
from .forms import *
from django.http import JsonResponse
from django.db.models import Q
from requests.structures import CaseInsensitiveDict
import requests

from django.core.exceptions import ObjectDoesNotExist
from messaging.models import Messaging
from html import escape


# Create your views here.

@login_required()
@user_passes_test(lambda u: u.age >= 18)
def AddService(request):
    provider = request.user
    if request.method == 'POST':
        serviceform = ServiceForm(request.POST)
        if serviceform.is_valid():
            serviceform.save()
            messages.success(request,
                             'Your service has been submitted to The ApplyPeer Admin Team for approval.'
                             ' Once this has been approved, you will receive an email notification.')
            return redirect('bookings:ListService')
    else:
        serviceform = ServiceForm()

    context = {
        'form': serviceform,
    }
    return render(request, 'services/edit-service.html', context)


@login_required()
@user_passes_test(lambda u: u.age >= 18)
def EditService(request, pk):
    obj = Services.objects.get(id=pk)
    if request.method == 'POST':
        form = ServiceUpdateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('bookings:ListService')
    else:
        form = ServiceUpdateForm(instance=obj)
    context = {
        'form': form,
        'edit': "True",
    }
    return render(request, 'services/edit-service.html', context)


def ListServices(request):
    if request.user.user_type == 4:
        obj = UserServices.objects.all()
        context = {
            'list': obj,
        }
    elif request.user.user_type == 0 or request.user.user_type == 11:
        obj = Services.objects.all()
        context = {
            'supe_list': obj,
        }

    return render(request, 'services/services-list.html', context)


@login_required()
@user_passes_test(lambda u: u.age > 17)
def MentorAddService(request):
    if request.user.user_type == 4:
        mentor = Mentor.objects.get(admin=request.user)
        if mentor.profile_status:
            paypal_acc = PaypalOnboardedSeller.objects.filter(user=request.user, permission_granted=True,paypal_account_email_confirmed=True)

            merchant_id = request.GET.get('merchantIdInPayPal')
            account_status = request.GET.get('accountStatus')

            permission_granted = request.GET.get('permissionsGranted')
            consent_status = request.GET.get('consentStatus')
            email_confirmed = request.GET.get('isEmailConfirmed')

            if merchant_id and permission_granted and consent_status and email_confirmed and account_status:
                if permission_granted == 'true':
                    permission_granted = True
                elif permission_granted == 'false':
                    permission_granted = False
                if consent_status == 'true':
                    consent_status = True
                elif consent_status == 'false':
                    consent_status = False
                if email_confirmed == 'true':
                    email_confirmed = True
                elif email_confirmed == 'false':
                    email_confirmed = False
                paypal_seller_onboarded = PaypalOnboardedSeller.objects.create(
                    user=request.user, paypal_merchant_id=merchant_id, paypal_account_status=account_status,
                    permission_granted=permission_granted, consent_status=consent_status,
                    paypal_account_email_confirmed=email_confirmed
                )
                paypal_seller_onboarded.save()
                # TODO: ADD MORE ELIFs TO VERIFY PERMISSIONS ARE GRANTED!
        else:
            return redirect('administration:page_not_found')
    else:
        return redirect('administration:page_not_found')
    if request.method == 'POST':
        form = UserServicesForm(request.POST)
        print(request.POST)
        if form.is_valid():
            user_service = form.save(commit=False)
            user_service.provider = request.user
            user_service.save()
            return redirect('administration:dashboard')
        else:
            pass

    form = UserServicesForm()
    context = {
        'form': form, 'paypal_acc': paypal_acc, 'merchant_id': merchant_id,
        'permission_granted': permission_granted, 'consentStatus': consent_status,
        'email_confirmed': email_confirmed, 'account_status': account_status
    }
    return render(request, 'services/edit-service.html', context)


@login_required()
def Booking(request):  # , slug

    if request.is_ajax and request.method == 'POST':
        data = request.POST
        post_data = data.dict()
        student_id = post_data['student']
        stu = StudentPersonalInformation.objects.using('afm_personal_information').get(
            id=student_id)
        student = CustomUser.objects.get(slug=stu.admin.user_slug)
        minutes = post_data['duration']
        from_t = post_data['time']
        from_time = datetime.strptime(from_t, '%H:%M')
        final_time = from_time + timedelta(minutes=int(post_data['duration']))
        service = Services.objects.get(id=post_data['selected_service'])
        original_date = datetime.strptime(post_data['date'], '%m-%d-%Y')
        date = original_date.strftime("%Y-%m-%d")
        app = Appointment.objects.create(
            provider=request.user, booker=student, date=date,
            from_time=from_time, to_time=final_time, status='Pending',
            services=service, cost=0, currency='USD',
            Details=post_data['detail'], duration_minutes=post_data['duration']
        )

        # return JsonResponse({'link': f'https://applyforinternship-sillr.ondigitalocean.app/booking/confirm/{app.id}'}, status=200)
        # return JsonResponse({
        #                         'link': f'<a target=blank, href="https://alumni.intfoundationgroup.co.uk/booking/confirm/{app.id}/">{request.user.first_name} sent you an offer, click here to accept</a>'},
        #                     status=200)
        # link = f"{request.user.first_name} sent you an offer, click <a href='https://alumni.intfoundationgroup.co.uk/booking/confirm/{app.id}/' > here</a> to accept"
        link = f"{request.user.first_name} sent you an offer, click <a href='https://alumni.intfoundationgroup.co.uk/booking/confirm/{app.id}/' > here</a> to accept"
        return JsonResponse({
            'link': link},
            status=200)


@login_required()
def ApproveAppointment(request, pk):
    obj = Appointment.objects.get(id=pk)
    if not obj.booker == request.user:
        return redirect('administration:page_not_found')
        
    if request.is_ajax and request.method == 'POST':
        data = request.POST
        post_data = data.dict()
        cost = int(post_data['cost'])
        if cost == 0 and obj.booker == request.user:
            obj.status = 'Approved'
            obj.save()
        elif cost > 0:
            try:
                paypal_acc = PaypalOnboardedSeller.objects.get(user=obj.provider, permission_granted=True,
                                                               paypal_account_email_confirmed=True)
                paypal_merchant_id = paypal_acc.paypal_merchant_id
            except ObjectDoesNotExist:
                paypal_merchant_id = None
        return JsonResponse({'yay': 'bababooey'}, status=200)
    else:
        try:
            paypal_acc = PaypalOnboardedSeller.objects.get(user=obj.provider, permission_granted=True,
                                                           paypal_account_email_confirmed=True)
            paypal_merchant_id = paypal_acc.paypal_merchant_id
        except ObjectDoesNotExist:
            paypal_merchant_id = None
        return render(request, 'appointments/book.html', {'appointment': obj, 'paypal_merchant_id': paypal_merchant_id,
                                                          'link': 'https://alumni.intfoundationgroup.co.uk/'})


@login_required()
def BookingHistory(request):
    obj = Appointment.objects.filter(Q(booker=request.user) | Q(provider=request.user))
    context = {
        'appointment': obj,
    }
    return render(request, 'core/bookinghistory.html', context)


@login_required()
def AppointmentsList(request):
    if request.user.user_type == 4:

        obj = Appointment.objects.filter(provider=request.user).order_by('-id')

    elif request.user.user_type == 3 or request.user.user_type == 5:

        obj = Appointment.objects.filter(booker=request.user).order_by('-id')

    elif request.user.user_type == 0 or request.user.user_type == 11:
        obj = Appointment.objects.filter(status='Approved').order_by('date')

    elif request.user.user_type == 11:
        school = request.user.school
        students = Student.objects.filter(school=school).values_list('id', flat=True)
        mentors = Mentor.objects.filter(school=school).values_list('id', flat=True)

        obj = Appointment.objects.filter(Q(booker_id__in=students) | Q(provider_id__in=mentors))

    tz = pytz.timezone(request.user.timezone)
    for o in obj:
        # aware_dt = datetime.combine(datetime.today(), o.from_time).replace(tzinfo=timezone.utc)
        # time_str = aware_dt.strftime('%H:%M')
        # time_obj = datetime.strptime(time_str, '%H:%M').time()


        o.from_time = time_tz_conversion(tz, o.from_time)
        o.to_time = time_tz_conversion(tz, o.to_time)
        print(type(o.from_time))
        print(type(o.to_time))
        print(o.from_time)
        print(o.to_time)
        if o.from_time.tzinfo is not None:
            print("The datetime object is aware.")
        else:
            print("The datetime object is naive.")

        if o.to_time.tzinfo is not None:
            print("The datetime object is aware.")
        else:
            print("The datetime object is naive.")
    if request.method == 'POST':
        appointment = request.POST.get['id']
        Appointment.objects.get(id=appointment).update(status='Cancelled')

    context = {
        'list': obj,
    }
    return render(request, 'services/appointments-list.html', context)

@login_required()
def AdminAppointment(request, slug):
    if request.user.user_type == 0 or request.user.user_type == 11:
        user = CustomUser.objects.get(slug=slug)
        mentor = f'{user.first_name} {user.last_name}'
        form = AdminAppointmentForm(initial={'provider': mentor, 'provider_id': user})
        if request.method == 'POST':
            form = AdminAppointmentForm(data=request.POST)
            if form.is_valid():
                from_t = request.POST.get('time')
                from_time = datetime.strptime(from_t, '%H:%M')
                final_time = from_time + timedelta(minutes=int(request.POST.get('duration_minutes')))
                obj = form.save(commit=False)
                obj.to_time = final_time
                obj.from_time = from_time
                obj.save()
                # new_msg = Messaging(sender=request.user, receiver=receiver_profile, comment=msg)
                link = f"{obj.provider.first_name} sent you an offer, click <a href='https://alumni.intfoundationgroup.co.uk/booking/confirm/{obj.id}/' > here</a> to accept"
                Messaging.objects.create(sender=obj.provider, receiver=obj.booker, comment=link)
                messages.success(request, "appointment created successfully")
                return redirect('administration:dashboard')


    return render(request, 'appointments/admin_appointment.html', {'form': form})


def SetAvailability(request):
    current_date = datetime.now()
    last_date = current_date + relativedelta(months=+3)
    i = 0
    while current_date < last_date:
        get_day = current_date.strftime("%A")
        i = i + 1
        if request.POST.get('Monday') and get_day == 'Monday':
            try:
                Timeslots.objects.create(available=True, from_time=request.POST.get('monday-from'),
                                         to_time=request.POST.get('monday-to'), date=current_date,
                                         provider=request.user)
            except:
                pass
        if request.POST.get('Tuesday') and get_day == 'Tuesday':
            try:
                Timeslots.objects.create(available=True, from_time=request.POST.get('tuesday-from'),
                                         to_time=request.POST.get('tuesday-to'), date=current_date,
                                         provider=request.user)
            except:
                pass
        if request.POST.get('Wednesday') and get_day == 'Wednesday':
            try:
                Timeslots.objects.create(available=True, from_time=request.POST.get('wednesday-from'),
                                         to_time=request.POST.get('wednesday-to'), date=current_date,
                                         provider=request.user)
            except:
                pass
        if request.POST.get('Thursday') and get_day == 'Thursday':
            try:
                Timeslots.objects.create(available=True, from_time=request.POST.get('thursday-from'),
                                         to_time=request.POST.get('thursday-to'), date=current_date,
                                         provider=request.user)

            except:
                pass
        if request.POST.get('Friday') and get_day == 'Friday':
            try:
                Timeslots.objects.create(available=True, from_time=request.POST.get('friday-from'),
                                         to_time=request.POST.get('friday-to'), date=current_date,
                                         provider=request.user)
            except:
                pass
        if request.POST.get('Saturday') and get_day == 'Saturday':
            try:
                Timeslots.objects.create(available=True, from_time=request.POST.get('saturday-from'),
                                         to_time=request.POST.get('saturday-to'), date=current_date,
                                         provider=request.user)
            except:
                pass
        if request.POST.get('Sunday') and get_day == 'Sunday':
            try:
                Timeslots.objects.create(available=True, from_time=request.POST.get('sunday-from'),
                                         to_time=request.POST.get('sunday-to'), date=current_date,
                                         provider=request.user)
            except:
                pass
        current_date = current_date + relativedelta(days=+1)
    # if current_date == last_date:
    #     messages.success(request, 'Availability added successfully.')
    # else:
    #     messages.error(request, 'Availability not added successfully.')
    print('---------------',AvailabilityForm())
    return render(request, 'services/availability.html', {'form': AvailabilityForm()})


def UpdateAvailablilty(request):
    msg = ''
    queryset = Timeslots.objects.filter(provider=request.user)

    if not queryset:
        msg = "You didn't set any availability"
    if request.method == 'POST':
        check = request.POST.get('unavail')
        if check:
            date = request.POST.get('date')
            start = request.POST.get('from')
            end = request.POST.get('to')
            try:
                timeslot = Timeslots.objects.get(date=date, provider=request.user)
                timeslot.available = "False"
                timeslot.save()
            except:
                pass
        else:
            date = request.POST.get('date')
            start = request.POST.get('from')
            end = request.POST.get('to')
            try:
                timeslot = Timeslots.objects.get(date=date, provider=request.user)
                timeslot.from_time = start
                timeslot.to_time = end
                timeslot.save()
            except:
                pass
        holidays = request.POST.get('holiday')
        if holidays:
            from_time = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            from_date = datetime.strptime(from_time, "%Y-%m-%d")
            to_date = datetime.strptime(to_date, "%Y-%m-%d")
            while from_date < to_date:
                Timeslots.objects.filter(date=from_date, provider=request.user).delete()
                queryset = Appointment.objects.filter(date=from_date, provider=request.user)
                for q in queryset:
                    q.status = "Cancelled"
                    q.save()
                from_date = from_date + relativedelta(days=+1)

    return render(request, 'services/update-availability.html', {'msg': msg})


def GetTimeslot(request):
    data = request.GET.get('data')
    get_time = Timeslots.objects.get(date=data, provider=request.user)
    from_time = get_time.from_time
    to_time = get_time.to_time
    data_list = {"start": from_time, "end": to_time}
    return JsonResponse({'instance': data_list}, status=200)


def GetSlots(request):
    data = request.GET.get('date')
    data2 = request.GET.get('user')
    h = request.GET.get('duration')

    delta = timedelta(minutes=int(h))

    minutes = delta.total_seconds() / 60

    user = get_user(data2)

    queryset = Timeslots.objects.filter(date=data, provider=user)


    appointments = Appointment.objects.filter(provider=user, date=data)
    time_list = []
    final_time = []

    for i in appointments:

        obj = datetime.strptime(str(i.from_time), "%H:%M:%S")
        to_time = i.to_time
        from_time = obj.time()
        time_list.append(str(from_time))
        final_time.append(str(to_time))

    data_list = []
    for q in queryset:

        from_time = q.from_time
        to_time = q.to_time
        start = datetime.strptime(str(from_time), "%H:%M:%S")
        end = datetime.strptime(str(to_time), "%H:%M:%S")
        min_gap = minutes
        arr = [(start + timedelta(hours=min_gap * i / 60)).strftime("%H:%M:%S")
               for i in range(int((end - start).total_seconds() / 60.0 / min_gap))]
        mid_list = []
        for j in range(0, len(time_list)):
            if not time_list:
                break;

            start = time_list[j]
            end = final_time[j]
            for m in range(0, len(arr)):
                mid = arr[m]
                result = time_in_range(start, end, mid)
                if result:
                    mid_list.append(arr[m])

        remove_list = time_list + mid_list

        for i in arr[:]:
            if not time_list:
                break;
            if i in remove_list:
                arr.remove(i)

        data_list.append(arr)
        slots = []
        new_data_list = [x[:-3] for x in data_list[0]]
        slots.append(new_data_list)

    data = json.dumps(data_list, indent=4, sort_keys=True, default=str)
    return JsonResponse({'instance': slots}, status=200)


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


def request_cancellation(request, pk):
    obj = Appointment.objects.get(id=pk)
    AppointmentCancelRequests.objects.create(Appointment=obj, Mentor=obj.provider)
    msg = 'Your cancellation request has been submitted to The ApplyPeer Admin Team for approval.'
    messages.success(request, msg)

    return JsonResponse(data=msg, status=200)


def admin_approve_cancellation(request, pk):
    obj = Appointment.objects.get(id=pk)
    obj.status = 'Cancelled'
    obj.AppointmentCancelRequests.approved = True
    obj.save()

    return JsonResponse(status=200)


