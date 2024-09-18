from datetime import datetime, timedelta, timezone
import re

import pytz

from bookings.models import Appointment
from administration.models import CustomUser


def time_tz_conversion(tz, time):
    # aware_dt = datetime.combine(datetime.today(), time).replace(tzinfo=timezone.utc)
    return datetime.combine(datetime.today(), time).replace(tzinfo=timezone.utc)


def annotate_appointment(queryset):
    regex = re.compile('booking/confirm/[0-9]*/')
    for each in queryset:
        if '/booking/confirm/' in each.comment:
            if regex.findall(each.comment):
                each.appointment = Appointment.objects.get(id=re.findall("\d+", regex.findall(each.comment)[0])[0])
            else:
                each.appointment = None
        else:
            each.appointment = None
    # print("queryset")
    # for each in queryset:
    #     print(each.comment)
    #     print(each.appointment)
    # print("queryset")
    return queryset


def get_user(id):
    return CustomUser.objects.get(id=id)