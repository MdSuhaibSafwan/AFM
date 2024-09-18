from django.urls import path
from .views import *
# from django.views.generic import TemplateView
# TemplateView.as_view()
app_name = 'payments'

urlpatterns = [
    path('paypal-onboarding/', PaypalSellerOnboarding, name='paypal-onboarding'),
    path('paypal-payment-status/', PayPalPaymentStatus, name='paypal-payment-status'),
    path('paypal-onboarded-sellers-list/', OnboardedPayPalSellerLisView, name='paypal_sellers'),
    path('paypal-transactions-list/', PayPalTransactionsLisView, name='paypal_transactions'),
    path('paypal-webhooks/', PayPalWebhooksView, name='paypal_webhooks'),
]