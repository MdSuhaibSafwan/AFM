# AFM/asgi.py
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AFM.settings')

from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()


from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from .routing import websocket_urlpatterns
from channels.security.websocket import AllowedHostsOriginValidator

from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from .websocket_auth import WebsocketMiddleware
from rest_framework.authtoken.models import Token

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            WebsocketMiddleware(
                URLRouter(
                    websocket_urlpatterns
                )
            )
        )
    ),
})
