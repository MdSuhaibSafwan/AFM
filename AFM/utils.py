import string
import random


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        # slug = slugify(instance.title)
        slug = random_string_generator(size=8)
    Klass = instance.__class__

    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        new_slug = "{randstr}".format(
            slug=slug, randstr=random_string_generator(size=8))

        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


from threading import current_thread
from django.utils.deprecation import MiddlewareMixin

_requests = {}


def get_current_request():
    t = current_thread()
    if t not in _requests:
        return None
    return _requests[t]


class RequestMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _requests[current_thread()] = request


