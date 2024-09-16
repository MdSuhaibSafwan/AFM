from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.authtoken.models import Token
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
import time


User = get_user_model()

@database_sync_to_async
def get_user_from_query_string(query_string):
    params = parse_qs(query_string.decode())
    token_key = params.get('token', [None])[0]
    return User.objects.first()

    if token_key:
        try:
            token = Token.objects.get(key=token_key)

            return token.user
        except Token.DoesNotExist:
            return None


class WebsocketMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):
        # Fetch user or some data from the database asynchronously
        # Call the next middleware or the consumer
        return await super().__call__(scope, receive, send)

class TokenAuthMiddlewareInstance:
    def __init__(self, inner, scope):
        self.inner = inner
        self.scope = scope

    async def __call__(self, receive, send):
        user = getattr(self.scope, "user", None)
        if user is None:
            query_string = self.scope['query_string']
            user = await get_user_from_query_string(query_string)
            self.scope['user'] = user or AnonymousUser()
            print("User: ", self.scope["user"])
            return await self.inner(self.scope, receive, send)

        if user.is_authenticated:
            return await self.inner(self.scope, receive, send)
        
        self.scope['user'] = AnonymousUser()
        return await self.inner(self.scope, receive, send)
