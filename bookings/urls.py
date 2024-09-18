from django.urls import path
from .views import *

app_name = 'bookings'

urlpatterns = [

    path('booking-history', BookingHistory, name='bookinghistory'),
    path('booking/', Booking, name='booking'),
    # path('set-availability/', SetAvailability, name='SetAvailability'),
    path('<int:pk>/', EditService, name='EditService'),
    path('add-service', AddService, name='AddService'),
    path('services/', ListServices, name='ListService'),
    path('mentor-service/', MentorAddService, name='MentorAddService'),
    # path('update-availability/', UpdateAvailablilty, name='UpdateAvailablilty'),
    # path('get-timeslot', GetTimeslot, name='ajax_timeslot'),
    path('get-slot', GetSlots, name='ajax_slot'),
    path('appointment/', AppointmentsList, name='appointment'),
    path('confirm/<int:pk>/', ApproveAppointment, name='approve-appointment'),
    path('admin-appointment/<slug:slug>/', AdminAppointment, name='admin_appointment'),

    path('set-availability/', SetAvailability, name='SetAvailability'),
    path('update-availability/', UpdateAvailablilty, name='UpdateAvailablilty'),
    path('get-timeslot', GetTimeslot, name='ajax_timeslot'),

    path('cancel/request/<int:pk>/', request_cancellation, name='request-cancellation'),
    path('cancel/approve/<int:pk>/', admin_approve_cancellation, name='approve-cancellation'),
]

from django.views.generic import TemplateView
urlpatterns += [
    path('foo/', TemplateView.as_view(template_name='foo.html'))
]