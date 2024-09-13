# Generated by Django 3.1.4 on 2022-10-10 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paypalonboardedseller',
            name='paypal_merchant_id',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='paypalonboardedseller',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paypalpayment',
            name='payment_id',
            field=models.CharField(max_length=50),
        ),
    ]
