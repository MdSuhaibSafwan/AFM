# Generated by Django 3.1.4 on 2022-09-02 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0005_customuser_timezone'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='how_did_you_hear_about_us',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
