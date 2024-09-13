from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blogs.models import Post

def custom_page_not_found_view(request, exception):
    return render(request, "404/404.html")


def custom_error_view(request, exception=None):
    return render(request, "404/404.html")


def custom_permission_denied_view(request, exception=None):
    return render(request, "404/404.html")


def custom_bad_request_view(request, exception=None):
    return render(request, "404/404.html")


def my_login_view(request, exception=None):
    return redirect('login')


class MySignupView(SignupView):

    # def get_context_data(self, **kwargs):
    #     ret = super(MySignupView, self).get_context_data(**kwargs)
    #     print('test data', ret)
    #     return ret

    def get(self, request):
        print('test', self['email'])
        return redirect('login')


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    ''' Login and redirect
    This is done in order to tackle the situation where user's email retrieved
    from one provider is different from already existing email in the database
    (e.g facebook and google both use same email-id). Specifically, this is done to
    tackle following issues:
    * https://github.com/pennersr/django-allauth/issues/215

    '''
    email_address = sociallogin.account.extra_data['email']
    User = get_user_model()
    users = User.objects.filter(email=email_address)
    if users:
        # allauth.account.app_settings.EmailVerificationMethod
        perform_login(request, users[0], email_verification='optional')
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL))


# @login_required
# def protected_serve(request, path, document_root=None, show_indexes=False):
#     return serve(request, path, document_root, show_indexes)


class Static_Sitemap(Sitemap):

    priority = 1.0
    changefreq = 'yearly'

    def items(self):
        return ['administration:home']

    def location(self, item):
        return reverse(item)

class Blog_Sitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(post_status=2).order_by('-created_on')

    def lastmod(self, obj):
        return obj.created_on