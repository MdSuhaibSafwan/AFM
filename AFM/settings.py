"""
Django settings for AFM project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from decouple import config
import sys
import dj_database_url

_ = lambda text: text


# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


SECRET_KEY = config('SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
DEVELOPMENT_MODE = config('DEVELOPMENT_MODE')
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # stock
    'django.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # custom apps
    'administration',
    'application',
    'personal_information',
    'django_countries',
    'feedback',
    'faqs',
    'messaging',
    'bookings',
    'payments',
    'page',

    # 3rd party apps
    'crispy_forms',
    'widget_tweaks',
    'blogs',
    'notifications',
    'rest_framework',
    'ckeditor',
    'django_summernote',
    'django_social_share',
    'webpush',
    'gdpr_cookie_consent',

    #allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'captcha',
    'django.contrib.sitemaps',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'AFM.utils.RequestMiddleware',
    # 'social_django.middleware.SocialAuthExceptionMiddleware',
]


# Webpush VAPID_KEY Generated from https://web-push-codelab.glitch.me/
WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BCLgMgNUwK6Jm78-w00qgFdG99I3vpAOvlGjpY4b8PUcAKXYthDuWiogwlVmdHJj0d2agZE1ZkjXxYHGkaz7JLU",
    "VAPID_PRIVATE_KEY": "gLrurlLSn5-bjwTF1HsJVfok68sW_01ySoHYAw0mSv8",
    "VAPID_ADMIN_EMAIL":  "viralsolanki2@gmail.com"
}

ROOT_URLCONF = 'AFM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'administration.context_processors.current_pi_user',
                'administration.context_processors.current_user',
                # 'social_django.context_processors.backends',  # <-- Social media authentication
                # 'social_django.context_processors.login_redirect',  # <-- Social media authentication

            ],
        },
    },
]

WSGI_APPLICATION = 'AFM.wsgi.application'
CRISPY_TEMPLATE_PACK = 'uni_form'

# drag and drop file
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if DEVELOPMENT_MODE:
    DATABASES = {

        # 'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / "default.sqlite3",
        # },
        # 'default': {},
        # 'afm': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / "afm.sqlite3",
        # },
        # 'afm_personal_information': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / "afm_personal_information.sqlite3",
        # },

        'default': dj_database_url.parse(config('DATABASE_URL_GENERAL')),
        # 'afm': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / "afm.sqlite3",
        #     # 'NAME': config('DB_AFM'),
        #     # 'USER': config('DB_AFM_USER'),
        #     # 'PASSWORD': config('DB_AFM_PASSWORD'),
        #     # 'HOST': config('DB_AFM_HOST'),
        #     # 'PORT': config('DB_AFM_PORT'),
        # },
        # 'afm_personal_information': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': BASE_DIR / "afm_p.sqlite3",
        #     # 'NAME': config('DB_personal_information'),
        #     # 'USER': config('DB_personal_information_USER'),
        #     # 'PASSWORD': config('DB_personal_information_PASSWORD'),
        #     # 'HOST': config('DB_personal_information_HOST'),
        #     # 'PORT': config('DB_personal_information_PORT'),
        # }
        'afm': dj_database_url.parse(config('DATABASE_URL_GENERAL')),
        'afm_personal_information': dj_database_url.parse(config('DATABASE_URL_PERSONAL')),
    }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
    if config('DATABASE_URL_GENERAL', None) is None or config('DATABASE_URL_PERSONAL', None) is None:
        raise Exception("DATABASE_URL environment variable not defined")
    DATABASES = {
        'default': {},
        'afm': dj_database_url.parse(config('DATABASE_URL_GENERAL')),
        'afm_personal_information': dj_database_url.parse(config('DATABASE_URL_PERSONAL')),
    }

import random


class AuthRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = {'administration', 'application', 'sessions', 'contenttypes', 'auth', 'admin', 'sites',
                        'django_email_verification', 'feedback', 'faqs', 'blogs', 'notifications', 'captcha',
                        'storages', 'webpush', 'messaging', 'gdpr_cookie_consent','allauth', 'account',
                        'socialaccount', 'bookings', 'payments', 'page'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'afm'
        return None
        # return 'afm'

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'afm'
        return None
        # return 'afm'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.route_app_labels or
                obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'afm' database.
        """
        if app_label in self.route_app_labels:
            return db == 'afm'
        return None


import random


class Afm_personal_information_router:

    def db_for_read(self, model, **hints):
        """
        Reads go to a randomly-chosen replica.
        """
        # return random.choice(['afm_personal_information'])
        return 'afm_personal_information'

    def db_for_write(self, model, **hints):
        """
        Writes always go to primary.
        """
        return 'afm_personal_information'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Relations between objects are allowed if both objects are
        in the primary/replica pool.
        """
        db_set = {'afm', 'afm_personal_information'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        All non-auth models end up in this pool.
        """
        if app_label == 'personal_information':
            return db == 'afm_personal_information'
        return None


DATABASE_ROUTERS = ['AFM.settings.AuthRouter', 'AFM.settings.Afm_personal_information_router']

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}

MESSAGES_TO_LOAD = 1000


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'Europe/London'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

SITE_ID = 1

AUTH_USER_MODEL = 'administration.CustomUser'
LOGIN_REDIRECT_URL = 'administration:dashboard'
LOGOUT_REDIRECT_URL = 'administration:login'
LOGIN_URL = 'administration:login'

# SOCIAL_AUTH_GITHUB_KEY = config('SOCIAL_AUTH_GITHUB_KEY')
# SOCIAL_AUTH_GITHUB_SECRET = config('SOCIAL_AUTH_GITHUB_SECRET')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'post_office.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
MAIL_SEND_FROM = config('MAIL_SEND_FROM', default=EMAIL_HOST_USER)

# Google Captcha
RECAPTCHA_PUBLIC_KEY = config('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = config('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_REQUIRED_SCORE = 0.85

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/")
]
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# from AFM.aws.conf import *

# ---------------- Chat catch -------------------------------
# ASGI_APPLICATION = "AFM.routing.application"
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }

# ------------------ Email verification --------------------------

HTML_MESSAGE_TEMPLATE = "registration/email_verification.html"

VERIFICATION_SUCCESS_TEMPLATE = "registration/email_verification_success.html"

VERIFICATION_FAILED_TEMPLATE = "registration/email_verification_failed.html"
SUBJECT = 'AFM Verify Your Email'

CRISPY_TEMPLATE_PACK ='bootstrap4'

# -------------------- ckeditor -------------------------
CKEDITOR_BASEPATH = "/my_static/ckeditor/ckeditor/"

CKEDITOR_UPLOAD_PATH = "uploads/"


COOKIE_CONSENT_SETTINGS = {
    # Base template will be used for the cookie management view.
    # It should contain {% block content %}{% endblock %}
    "base_template_name": "registration/reg_base.html",

    # Description will be used in the modal dialog and cookie management view.
    # Provide either a translatable string or a HTML template name.
    "description": _(""),
    "description_template_name": "gdpr_cookie_consent/descriptions/what_are_cookies.html",

    # Extra information will be used at the end of cookie management view.
    # Provide either a translatable string or a HTML template name.
    "extra_information": _(""),
    "extra_information_template_name": "gdpr_cookie_consent/descriptions/extra.html",

    # All important elements will have CSS classes with `cc-` prefix,
    # by which you can target them and overwrite their styling.
    # But you can attach some CSS classes to certain elements too.
    "styling": {
        "primary_button_css_classes": "primary-button",
        "secondary_button_css_classes": "secondary-button",
        "provider_list_css_classes": "",
        "provider_item_css_classes": "",
        "link_css_classes": "",
        "section_anchor_css_classes": "",
    },
    # Any variables that will be passed to conditional HTML snippets
    "extra_context": {
        "FUNCTIONALITY_COOKIE_VALUE": "🛠",
        "PERFORMANCE_COOKIE_VALUE": "📊",
        "MARKETING_COOKIE_VALUE": "📢",
    },

    # Consent cookie max age say how many seconds to keep the cookie consent preferences.
    # For example, it can be approximately six months
    "consent_cookie_max_age": 60 * 60 * 24 * 30 * 6,

    # Sections define the purposes of cookie groups.
    # For example: Essential, Functionality, Performance, and Marketing
    "sections": [
        {
            # The slug will be used as a readable identifier of the section
            "slug": "essential",

            # Translatable title of the section
            "title": _("Essential Cookies"),

            # Required sections will be already selected and read-only
            "required": True,

            # Section summary will be shown in the modal dialog and preferences form.
            # Provide either a translatable string or a HTML template name.
            "summary": _(
                "These cookies are always on, as they’re essential for making this website work, and making it safe. Without these cookies, services you’ve asked for can’t be provided."),
            "summary_template_name": "",

            # Section description will be used at the extended cookie explanation in the cookie management view.
            # Provide either a translatable string or a HTML template name.
            "description": _(
                "These cookies are always on, as they’re essential for making this website work, and making it safe. Without these cookies, services you’ve asked for can’t be provided."),
            "description_template_name": "",

            # Cookie providers are websites that set the cookies on your website
            "providers": [
                {
                    # Translatable title of the provider
                    "title": _("Apply for Medicine"),

                    # Provider description will be used at the extended cookie explanation in the cookie management view.
                    # Provide either a translatable string or a HTML template name.
                    "description": "",
                    "description_template_name": "",

                    # A list of cookies set by the provider
                    "cookies": [
                        {
                            # Cookie name can include wildcard syntax like "abc_*"
                            "cookie_name": "sessionid",

                            # Human-readable translated duration of the cookie
                            "duration": _("2 Weeks"),

                            # Cookie description will be used at the extended cookie explanation in the cookie management view.
                            # Provide either a translatable string or a HTML template name.
                            "description": _(
                                "Session ID used to authenticate you and give permissions to use the site."),
                            "description_template_name": "",

                            # Cookie domain will be used to delete cookies if a section is unchecked
                            "domain": "applyformedicine.com",
                        },
                        {
                            "cookie_name": "csrftoken",
                            "duration": _("Session"),
                            "description": _(
                                "Security token used to ensure that no hackers are posting forms on your behalf."),
                            "description_template_name": "",
                            "domain": "applyformedicine.com",
                        },
                        {
                            "cookie_name": "cookie_consent",
                            "duration": _("6 Years"),
                            "description": _("Settings of Cookie Consent preferences."),
                            "description_template_name": "",
                            "domain": "applyformedicine.com",
                        },
                    ]
                },
            ],
        },
        {
            "slug": "functionality",
            "title": _("Functionality Cookies"),

            # Conditional HTML snippet will be loaded or rendered if this section is selected
            "conditional_html_template_name": "conditional_html/functionality.html",
            "required": False,
            "summary": _(
                "These cookies help us provide enhanced functionality and personalisation, and remember your settings. They may be set by us or by third party providers."),
            "summary_template_name": "",
            "description": _(
                "These cookies help us provide enhanced functionality and personalisation, and remember your settings. They may be set by us or by third party providers."),
            "description_template_name": "",
            "providers": [
                {
                    "title": _("Apply for Medicine"),
                    "description": _(""),
                    "description_template_name": "",
                    "cookies": [
                        {
                            "cookie_name": "functionality_cookie",
                            "duration": _("Session"),
                            "description": "",
                            "description_template_name": "",
                            "domain": "applyformedicine.com",
                        },
                    ]
                },
            ],
        },
        {
            "slug": "performance",
            "title": _("Performance Cookies"),
            "conditional_html_template_name": "conditional_html/performance.html",
            "required": False,
            "summary": _(
                "These cookies help us analyse how many people are using this website, where they come from and how they're using it. If you opt out of these cookies, we can’t get feedback to make this website better for you and all our users."),
            "summary_template_name": "",
            "description": _(
                "These cookies help us analyse how many people are using this website, where they come from and how they're using it. If you opt out of these cookies, we can’t get feedback to make this website better for you and all our users."),
            "description_template_name": "",
            "providers": [
                {
                    "title": _("Apply for Medicine"),
                    "description": _(""),
                    "description_template_name": "",
                    "cookies": [
                        {
                            "cookie_name": "performance_cookie",
                            "duration": _("Session"),
                            "description": "",
                            "description_template_name": "",
                            "domain": "applyformedicine.com",
                        },
                    ]
                },
            ],
        },
        {
            "slug": "marketing",
            "title": _("Marketing Cookies"),
            "conditional_html_template_name": "conditional_html/marketing.html",
            "required": False,
            "summary": _(
                "These cookies are set by our advertising partners to track your activity and show you relevant ads on other sites as you browse the internet."),
            "summary_template_name": "",
            "description": _(
                "These cookies are set by our advertising partners to track your activity and show you relevant ads on other sites as you browse the internet."),
            "description_template_name": "",
            "providers": [
                {
                    "title": _("Apply for Medicine"),
                    "description": _(""),
                    "description_template_name": "",
                    "cookies": [
                        {
                            "cookie_name": "marketing_cookie",
                            "duration": _("Session"),
                            "description": "",
                            "description_template_name": "",
                            "domain": "applyformedicine.com",
                        },
                    ]
                },
            ],
        },
    ]
}

# summernote setup

X_FRAME_OPTIONS = 'SAMEORIGIN'

SUMMERNOTE_CONFIG = {

    # You can completely disable the attachment feature.
    # 'disable_attachment': True,

    # You can put custom Summernote settings
    'summernote': {
        'toolbar': [
            ['style', []],
            ['font', []],
            ['fontname', []],
            ['color', []],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', []],
            ['insert', []],
            ['view', []],
        ],


    },

}


# CELERY STUFF
# BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'
# CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TIMEZONE = 'Europe/London'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


def TWFL_EMAIL():
    return None