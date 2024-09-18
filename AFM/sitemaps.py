from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blogs.models import Post
from personal_information.models import MentorPersonalInformation
from administration.models import Mentor
from administration.templatetags.administration_extras import getmentorprofileurl

class StaticSitemapMain(Sitemap):

    priority = 1.00
    # changefreq = 'yearly'

    def items(self):
        return ['administration:home',]

    def location(self, item):
        return reverse(item)


class StaticSitemap(Sitemap):

    priority = 0.80
    # changefreq = 'yearly'

    def items(self):
        return ['blogs:public_blog_list', 'administration:registration',
                'administration:contact_us', 'login','administration:medical_school_mentor',
                'administration:study_medicine',
                'administration:uk_medical_schools',
                'administration:parents',
                'administration:widening_access',
                'administration:study_medicine_in_ireland',
                'administration:study_medicine_in_europe',
                'administration:study_medicine_in_the_usa',
                'administration:study_medicine_in_canada',
                'administration:study_medicine_in_australia',
                'administration:study_medicine_in_the_caribbean',
                'administration:studying_medicine_at_the_university_of_aberdeen_school_of_medicine',
                'administration:studying_medicine_at_the_university_of_dundee',
                'administration:studying_medicine_at_the_university_of_st_andrews',
                'administration:studying_medicine_at_the_university_of_edinburgh',
                'administration:studying_medicine_at_the_university_of_glasgow',
                'administration:studying_medicine_at_newcastle_university',
                'administration:studying_medicine_at_the_university_of_sunderlandol',
                'administration:studying_medicine_at_lancaster_university',
                'administration:studying_medicine_at_the_university_of_central_lancashire_uclan',
                'administration:studying_medicine_at_edge_hill_university',
                'administration:studying_medicine_at_hull_york_medical_school',
                'administration:studying_medicine_at_the_university_of_leeds',
                'administration:studying_medicine_at_the_university_of_sheffield',
                'administration:studying_medicine_at_manchester',
                'administration:studying_medicine_at_the_university_of_liverpool',
                'administration:studying_medicine_at_the_university_of_lincoln',
                'administration:studying_medicine_at_keele_university',
                'administration:studying_medicine_at_the_university_of_nottingham',
                'administration:studying_medicine_at_the_university_of_leicester',
                'administration:studying_medicine_at_aston_university',
                'administration:studying_medicine_at_the_university_of_birmingham',
                'administration:studying_medicine_at_norwich_medical_school',
                'administration:studying_medicine_at_the_university_of_cambridge',
                'administration:studying_medicine_at_the_university_of_buckingham',
                'administration:studying_medicine_at_the_university_of_oxford',
                'administration:studying_medicine_at_the_university_of_bristol',
                'administration:studying_medicine_at_anglia_ruskin_university',
                'administration:studying_medicine_at_barts',
                'administration:studying_medicine_at_st_georges_university_of_london',
                'administration:studying_medicine_at_the_university_college_london_ucl',
                'administration:studying_medicine_at_kings_college_london_kcl',
                'administration:studying_medicine_at_imperial_college_london',
                'administration:studying_medicine_at_brunel_university_london',
                'administration:studying_medicine_at_kent_and_medway_medical_school',
                'administration:studying_medicine_at_brighton_and_sussex_medical_school',
                'administration:studying_medicine_at_the_university_of_southampton',
                'administration:studying_medicine_at_the_university_of_exeter',
                'administration:studying_medicine_at_peninsula_medical',
                'administration:studying_medicine_at_warwick',
                'administration:studying_medicine_at_swansea_university',
                'administration:studying_medicine_at_cardiff_university',
                'administration:studying_medicine_at_queens_university',
                'administration:studying_medicine_at_ulster_university',
                'administration:medical_school_admissions_tests',
                'administration:studying_medicine_at_university_college_dublin',
                'administration:studying_medicine_at_royal_college_of_surgeons',
                'administration:studying_medicine_at_trinity_college_dublin',
                'administration:studying_medicine_at_national_university_of_ireland',
                'administration:studying_medicine_at_university_of_limerick',
                'administration:studying_medicine_at_university_college_cork_ucc',
                'administration:studying_medicine_at_medical_university_sofia',
                'administration:studying_medicine_at_the_medical_university_of_silesia',
                'administration:studying_medicine_at_karolinska_institute',
                'administration:studying_medicine_at_charles_university',
                'administration:graduate_entry_to_medicine',
                'administration:terms_and_conditions',
                'administration:privacy_notice',
                'administration:cookies_policy',
                'administration:safeguarding_policy',
                'administration:online_safety',
                'administration:codes_of_conduct',
                'password_reset',
                ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return

class BlogSitemap(Sitemap):
    # changefreq = "monthly"
    priority = 0.80

    def items(self):
        queryset = Post.objects.filter(post_status=2).order_by('-updated_on')
        temp = []
        for i in queryset:
            temp.append(i.author.admin.slug)
        user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
            admin__user_slug__in=temp, currently_studying=6)
        temp = []
        for i in user_mentor_pi:
            temp.append(i.admin.user_slug)
        return Post.objects.filter(post_status=2, author__admin__slug__in = temp).order_by('-updated_on')

    # def location(self, obj):
    #     return f"/{obj.permalink}"

    def lastmod(self, obj):
        return obj.updated_on

class MentorProfileSitemap(Sitemap):
    # changefreq = "monthly"
    priority = 0.80

    def items(self):
        queryset = Mentor.objects.filter(profile_status=True)
        temp = []
        for i in queryset:
            temp.append(i.admin.slug)

        user_mentor_pi = MentorPersonalInformation.objects.using('afm_personal_information').filter(
            admin__user_slug__in=temp, currently_studying=6).order_by('-updated_at')

        return user_mentor_pi

    def location(self, obj):
        return getmentorprofileurl(obj.admin.user_slug, with_birth_domain=False)

        # if obj.url_slug:
        #     return reverse("administration:student_single_mentor_using_url_slug_twfl", kwargs={"slug": self.slug})
        # else:
        #     return reverse("administration:student_single_mentor_twfl", kwargs={"slug": self.slug})

    def lastmod(self, obj):
        return obj.updated_at


class StaticSitemap2(Sitemap):

    priority = 0.64
    # changefreq = 'yearly'

    def items(self):
        return [
                'administration:studying_medicine_at_the_university_of_aberdeen_school_of_medicine',
                'administration:studying_medicine_at_the_university_of_dundee',
                'administration:studying_medicine_at_the_university_of_st_andrews',
                'administration:studying_medicine_at_the_university_of_edinburgh',
                'administration:studying_medicine_at_the_university_of_glasgow',
                'administration:studying_medicine_at_newcastle_university',
                'administration:studying_medicine_at_the_university_of_sunderlandol',
                'administration:studying_medicine_at_lancaster_university',
                'administration:studying_medicine_at_the_university_of_central_lancashire_uclan',
                'administration:studying_medicine_at_edge_hill_university',
                'administration:studying_medicine_at_hull_york_medical_school',
                'administration:studying_medicine_at_the_university_of_leeds',
                'administration:studying_medicine_at_the_university_of_sheffield',
                'administration:studying_medicine_at_manchester',
                'administration:studying_medicine_at_the_university_of_liverpool',
                'administration:studying_medicine_at_the_university_of_lincoln',
                'administration:studying_medicine_at_keele_university',
                'administration:studying_medicine_at_the_university_of_nottingham',
                'administration:studying_medicine_at_the_university_of_leicester',
                'administration:studying_medicine_at_aston_university',
                'administration:studying_medicine_at_the_university_of_birmingham',
                'administration:studying_medicine_at_norwich_medical_school',
                'administration:studying_medicine_at_the_university_of_cambridge',
                'administration:studying_medicine_at_the_university_of_buckingham',
                'administration:studying_medicine_at_the_university_of_oxford',
                'administration:studying_medicine_at_the_university_of_bristol',
                'administration:studying_medicine_at_anglia_ruskin_university',
                'administration:studying_medicine_at_barts',
                'administration:studying_medicine_at_st_georges_university_of_london',
                'administration:studying_medicine_at_the_university_college_london_ucl',
                'administration:studying_medicine_at_kings_college_london_kcl',
                'administration:studying_medicine_at_imperial_college_london',
                'administration:studying_medicine_at_brunel_university_london',
                'administration:studying_medicine_at_kent_and_medway_medical_school',
                'administration:studying_medicine_at_brighton_and_sussex_medical_school',
                'administration:studying_medicine_at_the_university_of_southampton',
                'administration:studying_medicine_at_the_university_of_exeter',
                'administration:studying_medicine_at_peninsula_medical',
                'administration:studying_medicine_at_warwick',
                'administration:studying_medicine_at_swansea_university',
                'administration:studying_medicine_at_cardiff_university',
                'administration:studying_medicine_at_queens_university',
                'administration:studying_medicine_at_ulster_university',
                'administration:medical_school_admissions_tests',
                'administration:studying_medicine_at_university_college_dublin',
                'administration:studying_medicine_at_royal_college_of_surgeons',
                'administration:studying_medicine_at_trinity_college_dublin',
                'administration:studying_medicine_at_national_university_of_ireland',
                'administration:studying_medicine_at_university_of_limerick',
                'administration:studying_medicine_at_university_college_cork_ucc',
                'administration:studying_medicine_at_medical_university_sofia',
                'administration:studying_medicine_at_the_medical_university_of_silesia',
                'administration:studying_medicine_at_karolinska_institute',
                'administration:studying_medicine_at_charles_university',
                'administration:graduate_entry_to_medicine',
                'administration:terms_and_conditions',
                'administration:privacy_notice',
                'administration:cookies_policy',
                'administration:safeguarding_policy',
                'administration:online_safety',
                'administration:codes_of_conduct',
                'password_reset',
                ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, obj):
        return