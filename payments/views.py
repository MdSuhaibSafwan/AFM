from email import message
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from administration.models import CustomUser, Mentor, Student
from bookings.models import Appointment
from .models import *
import requests
from requests.structures import CaseInsensitiveDict
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
import json
from administration.login_check import super_admin_login_required, super_admin_user_required

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from paypalrestsdk import notifications

# PAYPAL CLIENT ID
# AbuWE-ONEloc8BCh2k11l-ig_7uBJkW_t0xuhq6jlLdACjO1-1zWQPtwUmEpzRDsZSV-Xs9fY4-Cl3jJ

# PAYPAL SECRET KEY
# EK-f6GiCZH_CJWE0nsDeyY8h0zoUEoy-Aw4mm8JwpIh2Bt3-DgzxcQCJy9kh4hPrvyIFcMorUTNUEpz_ 

# SANDBOX PERSONEL ACCOUNT:
# EMAIL: sb-kpxog10578867@personal.example.com
# PASS:  VSb@D_7i

# SANDBOX BUSINESS ACCOUNT:
# EMAIL: sb-97nhy10578864@business.example.com
# PASS:  Qqk48<I>

@login_required
def PaypalSellerOnboarding(request):
    if request.user.user_type == 4:
        mentor = Mentor.objects.get(admin=request.user)
        if mentor.profile_status:
            mentor_onboard_obj = PaypalOnboardedSeller.objects.filter(user=request.user)
            if mentor_onboard_obj.exists():
                messages.success(request, 'Your PayPal account is already Onboarded. Please contact support for further help.')
                return redirect('administration:dashboard')
            else:
                url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

                headers = CaseInsensitiveDict()
                headers["Accept"] = "application/json"
                headers["Accept-Language"] = "en_US"
                headers["Content-Type"] = "application/x-www-form-urlencoded"
                headers["Authorization"] = "Basic QWJ1V0UtT05FbG9jOEJDaDJrMTFsLWlnXzd1QkprV190MHh1aHE2amxMZEFDak8xLTF6V1FQdHdVbUVwelJEc1pTVi1YczlmWTQtQ2wzako6RUstZjZHaUNaSF9DSldFMG5zRGV5WThoMHpvVUVveS1BdzRtbThKd3BJaDJCdDMtRGd6eGNRQ0p5OWtoNGhQcnZ5SUZjTW9yVVROVUVwel8="

                data = "grant_type=client_credentials"
                resp = requests.post(url, headers=headers, data=data)
                json_resp = resp.json()
                access_token = json_resp['access_token']
                tracking_id = request.user.id
                headers = {
                    #  Already added when you pass json= but not when you pass data=
                    # 'Content-Type': 'application/json',
                    'Authorization': f'Bearer {access_token}',
                }
                json_data = {
                    'tracking_id': f'{tracking_id}',
                    'operations': [
                        {
                            'operation': 'API_INTEGRATION',
                            'api_integration_preference': {
                                'rest_api_integration': {
                                    'integration_method': 'PAYPAL',
                                    'integration_type': 'THIRD_PARTY',
                                    'third_party_details': {
                                        'features': [
                                            'PAYMENT',
                                            'REFUND',
                                        ],
                                    },
                                },
                            },
                        },
                    ],
                    'products': [
                        'EXPRESS_CHECKOUT',
                    ],
                    "partner_config_override": {
                        "return_url": "https://alumni.intfoundationgroup.co.uk/booking/mentor-service",
                    },
                    'legal_consents': [
                        {
                            'type': 'SHARE_DATA_CONSENT',
                            'granted': True,
                        },
                    ],
                }
                response = requests.post('https://api-m.sandbox.paypal.com/v2/customer/partner-referrals', headers=headers, json=json_data)
                complete_data = response.json()
                print(complete_data)
                self_url = complete_data['links'][0]['href']
                onboard_url = complete_data['links'][1]['href']
                return redirect(onboard_url)
        else:
            return redirect('administration:page_not_found')
    else:
        return redirect('administration:page_not_found')

@login_required
def PayPalPaymentStatus(request):
        if request.is_ajax and request.method == 'POST':
            data = request.POST
            post_data = data.dict()
            payment_id = post_data['transaction_id']
            payment_status = post_data['transaction_status']
            payment_ammount = post_data['transaction_amount']
            payment_currency = post_data['transaction_currency']
            payer = post_data['transaction_payer']
            payer_email = post_data['transaction_payer_email']
            appointment = post_data['appointment']

            if payment_status == 'COMPLETED':
                appointment = Appointment.objects.get(id=appointment)
                if float(payment_ammount) == float(appointment.cost) and request.user == appointment.booker:
                    paypal_payment = PaypalPayment.objects.create(
                        user = appointment.booker,payment_id=payment_id,
                        status=payment_status, amount_charged=payment_ammount,
                        currency=payment_currency,payer_paypal_name=payer,
                        payepayer_paypal_email=payer_email
                    )
                    paypal_payment.save()
            # TODO: elif payment_status == ''
        else:
            return redirect('administration:page_not_found')
        return HttpResponse(status=200) 

# TODO:
# CHECK ITS WORKING ON APPLYPEER!
# VERIFY PERMISSIONS ARE GRANTED!
def PayPalSellerOnboardingVerification(request):
    url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"

    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Accept-Language"] = "en_US"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Authorization"] = "Basic QWJ1V0UtT05FbG9jOEJDaDJrMTFsLWlnXzd1QkprV190MHh1aHE2amxMZEFDak8xLTF6V1FQdHdVbUVwelJEc1pTVi1YczlmWTQtQ2wzako6RUstZjZHaUNaSF9DSldFMG5zRGV5WThoMHpvVUVveS1BdzRtbThKd3BJaDJCdDMtRGd6eGNRQ0p5OWtoNGhQcnZ5SUZjTW9yVVROVUVwel8="

    data = "grant_type=client_credentials"


    resp = requests.post(url, headers=headers, data=data)

    json_resp = resp.json()
    access_token = json_resp['access_token']
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }
    partner_merchant_id = 'GET YOUR MERCHANT ID FROM: PayPal account > Settings > Business information > PayPal Merchant ID'
    seller_merchant_id = 'Query from DB after saving from URL Get Request!'
    response = requests.get('https://api-m.sandbox.paypal.com/v1/customer/partners/{partner_merchant_id}/merchant-integrations/{seller_merchant_id}', headers=headers)

# @method_decorator(csrf_exempt, name="dispatch")
@csrf_exempt
def PayPalWebhooksView(request):
    if request.method == 'POST':
        if "HTTP_PAYPAL_TRANSMISSION_ID" not in request.META:
            return HttpResponseBadRequest()

        auth_algo = request.META['HTTP_PAYPAL_AUTH_ALGO']
        cert_url = request.META['HTTP_PAYPAL_CERT_URL']
        transmission_id = request.META['HTTP_PAYPAL_TRANSMISSION_ID']
        transmission_sig = request.META['HTTP_PAYPAL_TRANSMISSION_SIG']
        transmission_time = request.META['HTTP_PAYPAL_TRANSMISSION_TIME']
        webhook_id =  '9JR1414457560630C' #settings.PAYPAL_WEBHOOK_ID
        event_body = request.body.decode(request.encoding or "utf-8")

        valid = notifications.WebhookEvent.verify(
            transmission_id=transmission_id,
            timestamp=transmission_time,
            webhook_id=webhook_id,
            event_body=event_body,
            cert_url=cert_url,
            actual_sig=transmission_sig,
            auth_algo=auth_algo,
        )

        if not valid:
            return HttpResponseBadRequest()

        webhook_event = json.loads(event_body)

        event_type = webhook_event["event_type"]
        print('ev: ',webhook_event)
        # CHECKOUT_ORDER_APPROVED = "CHECKOUT.ORDER.APPROVED"

        # if event_type == CHECKOUT_ORDER_APPROVED:
        #     print('hi')
    else:
        return redirect('administration:page_not_found')
    return HttpResponse(status=200) 
    
    
@super_admin_user_required
def OnboardedPayPalSellerLisView(request):
    obj = PaypalOnboardedSeller.objects.all()
    return render(request, 'payments/onboarded_sellers.html', {'obj':obj})
    
@super_admin_user_required
def PayPalTransactionsLisView(request):
    obj = PaypalPayment.objects.all()
    return render(request, 'payments/paypal_transactions.html', {'obj':obj})

# headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': 'Bearer ECvJ_yBNz_UfMmCvWEbT_2ZWXdzbFFQZ-1Y5K2NGgeHn',
        # }

        # data = '{ "url": "https://alumni.intfoundationgroup.co.uk/paypal-webhook/", "event_types": [ { "name": "CHECKOUT.CHECKOUT.BUYER-APPROVED" }, { "name": "CHECKOUT.ORDER.COMPLETED" }, { "name": "CHECKOUT.ORDER.VOIDED" }, { "name": "MERCHANT.ONBOARDING.COMPLETED" }, { "name": "ERCHANT.PARTNER-CONSENT.REVOKED" }, { "name": "CHECKOUT.ORDER.APPROVED" } ] }'

        # response = requests.post('https://api-m.sandbox.paypal.com/v1/notifications/webhooks', headers=headers, data=data)
        # print('Res: ',response)
        # event_url = response['links'][0]['href']
        # print('Self Link: ',event_url)