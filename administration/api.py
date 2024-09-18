from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import date, datetime, timedelta
from personal_information.models import CustomUserPersonalInformation, MentorPersonalInformation,StudentPersonalInformation, AppBasicInformation, SpokenLanguage, FoundationProvider

current_time = datetime.now().time()

class DemandAndSupply(APIView):
    def get(self, request, format=None, **kwargs):
        language = request.GET['language']
        country = request.GET['country']
        subject = request.GET['subject']
        # print(language,country,subject)
        mentors = MentorPersonalInformation.objects.filter(admin__spoken_languages__language = language,studying_in=country,currently_studying=subject).count()
        student = StudentPersonalInformation.objects.filter(admin__spoken_languages__language = language,study_destination=country,area_of_study=subject).count()
        print(student,mentors)
        data = {
            'demand':student,
            'supply':mentors,
        }
        return Response(data)
