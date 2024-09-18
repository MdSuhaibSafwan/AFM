"""AFM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from AFM.views import MySignupView, my_login_view, Blog_Sitemap, Static_Sitemap
from AFM.sitemaps import *

handler404 = 'AFM.views.custom_page_not_found_view'
handler500 = 'AFM.views.custom_error_view'
handler403 = 'AFM.views.custom_permission_denied_view'
handler400 = 'AFM.views.custom_bad_request_view'

sitemaps = {
    'home': StaticSitemapMain(),
    'static': StaticSitemap(),
    'post': BlogSitemap(),
    'mentor': MentorProfileSitemap(),
    'static2': StaticSitemap2(),
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('sitemap.xml',  sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('administration.urls', namespace='administration')),
    path('application/', include('application.urls', namespace='application')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('faqs/', include('faqs.urls', namespace='faqs')),
    path('med-school-blogs/', include('blogs.urls', namespace='blogs')),
    path('message/', include('messaging.urls', namespace='messaging')),
    # path('page/', include('page.urls', namespace='page')),
    path('inbox/notifications/', include('notifications.urls', namespace='notifications')),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        html_email_template_name='registration/password_reset_email.html'
    )),
    path('booking/', include('bookings.urls', namespace='booking')),
    path('summernote/', include('django_summernote.urls')),
    path('payment/', include('payments.urls', namespace='payments')),
    # override the SignupView of django-allauth
    path("social-accounts/social/signup/", view=MySignupView.as_view()),
    path("social-accounts/signup/", view=my_login_view),
    path("social-accounts/login/", view=my_login_view),
    path('accounts/', include('django.contrib.auth.urls')),
    path('social-accounts/', include('allauth.urls')),
    # path("select2/", include("django_select2.urls")),
    # path('captcha/', include('captcha.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('cookies/', include('gdpr_cookie_consent.urls', namespace='cookie_consent')),
    # url(r'^oauth/', include('social_django.urls', namespace='social')),
    re_path(r'^webpush/', include('webpush.urls')),
    # # url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    path('tz_detect/', include('tz_detect.urls')),
]
