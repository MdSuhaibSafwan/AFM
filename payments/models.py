from django.db import models
from administration.models import CustomUser


class PaypalOnboardedSeller(models.Model):
    user = models.ForeignKey(CustomUser, default=1, on_delete=models.PROTECT) # Areeb: removed blank,null & have set on_delete to models.PROTECT
    paypal_merchant_id = models.CharField(max_length=50) # Areeb: Increased Max length here.
    paypal_account_status = models.CharField(max_length=30)
    permission_granted = models.BooleanField(default=False)
    consent_status = models.BooleanField(default=False)
    paypal_account_email_confirmed = models.BooleanField(default=False)
    onboarded_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email


class PaypalPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)  # CustomUser objects not to be deleted in any case.
    payment_id = models.CharField(max_length=50) # Areeb: CHANGE from PositiveIntegerField TO CHARFIELD
    status = models.CharField(max_length=20)
    amount_charged = models.FloatField()
    currency = models.CharField(max_length=5)
    payer_paypal_name = models.CharField(max_length=50)
    payepayer_paypal_email = models.EmailField(max_length=50)
    paid_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
