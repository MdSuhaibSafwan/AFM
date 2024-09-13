# Generated by Django 3.2 on 2023-03-28 15:53

import AFM.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('personal_information', '0003_auto_20221130_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreferredCareerField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_career_field', models.CharField(max_length=200, null=True, unique=True)),
                ('status', models.BooleanField(default=True, null=True)),
                ('order_rank', models.PositiveIntegerField(default=0, null=True)),
            ],
            options={
                'ordering': ['-order_rank'],
            },
        ),
        migrations.CreateModel(
            name='PreferredLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_location', models.CharField(max_length=200, null=True, unique=True)),
                ('status', models.BooleanField(default=True, null=True)),
            ],
            options={
                'ordering': ['preferred_location'],
            },
        ),
        migrations.CreateModel(
            name='SkillsToDevelop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills_to_develop', models.CharField(max_length=200, null=True, unique=True)),
                ('status', models.BooleanField(default=True, null=True)),
            ],
            options={
                'ordering': ['skills_to_develop'],
            },
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='consent1',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='current_or_last_school_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='currently_living_in',
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='currently_studying',
            field=models.IntegerField(choices=[(0, 'NO'), (1, 'YES')], default=0, null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='last_qualification',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='level_of_english',
            field=models.IntegerField(choices=[('', 'Select'), (0, 'Beginners'), (1, 'Elementary'), (2, 'Intermediate'), (3, 'Advanced'), (4, 'Native Speaker')], null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='media_consent',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='mobile_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='appbasicinformation',
            name='what_are_you_studying',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='brp_card',
            field=models.FileField(blank=True, null=True, upload_to='documents/brp_card', validators=[AFM.validators.validate_file_size]),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='duration_of_internship',
            field=models.CharField(blank=True, choices=[('', 'Select'), ('1 Month', '1 Month'), ('2 Months', '2 Months'), ('3 Months', '3 Months'), ('4 Months', '4 Months')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='facebook_profile_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='follow_us_on_facebook',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='follow_us_on_instagram',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='follow_us_on_linkedin',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='follow_us_on_tiktok',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='follow_us_on_twitter',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='follow_us_on_youtube',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='instagram_profile_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='tiktok_profile_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='twitter_profile_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='university_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='url_slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='weekly_working_hours',
            field=models.CharField(blank=True, choices=[('', 'Select'), ('2 Hours', '2 Hours'), ('5 Hours', '5 Hours'), ('10 Hours', '10 Hours'), ('15 Hours', '15 Hours'), ('20 Hours', '20 Hours')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='where_will_you_be_during_the_completion_of_your_internship',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='would_you_like_us_to_generate_a_CV',
            field=models.IntegerField(blank=True, choices=[(0, 'NO'), (1, 'YES')], default=0, null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='youtube_shots',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='apppassportinformation',
            name='passport',
            field=models.FileField(null=True, upload_to='documents/', validators=[AFM.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='customuserpersonalinformation',
            name='profile_pic',
            field=models.FileField(null=True, upload_to='user_profile/', validators=[AFM.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='mentorpersonalinformation',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='documents/cv', validators=[AFM.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='mentorpersonalinformation',
            name='dbs_certificate',
            field=models.FileField(blank=True, null=True, upload_to='documents/dbs_certificate', validators=[AFM.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='mentorpersonalinformation',
            name='linkedin_profile_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mentorpersonalinformation',
            name='passport',
            field=models.FileField(null=True, upload_to='mentor_passports/', validators=[AFM.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='mentorpersonalinformation',
            name='student_id',
            field=models.FileField(blank=True, null=True, upload_to='user_profile/', validators=[AFM.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='mentorpersonalinformation',
            name='visa_card',
            field=models.FileField(blank=True, null=True, upload_to='documents/visa_card', validators=[AFM.validators.validate_file_size]),
        ),
        migrations.AlterField(
            model_name='mentorpersonalinformation',
            name='year_graduated',
            field=models.IntegerField(blank=True, choices=[('', 'Select'), (2021, 2021), (2022, 2022), (2023, 2023)], default=2023, null=True),
        ),
        migrations.AlterField(
            model_name='studentpersonalinformation',
            name='intake_year',
            field=models.IntegerField(choices=[('', 'Select'), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028)], null=True),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='preferred_career_field',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='personal_information.preferredcareerfield'),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='preferred_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='personal_information.preferredlocation'),
        ),
        migrations.AddField(
            model_name='mentorpersonalinformation',
            name='skills_to_develop',
            field=models.ManyToManyField(blank=True, to='personal_information.SkillsToDevelop'),
        ),
    ]
