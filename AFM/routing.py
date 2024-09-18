from django.urls import path
from messaging.consumers import ChatConsumer

websocket_urlpatterns = [
    path("messaging/", ChatConsumer.as_asgi(), ),
]   
