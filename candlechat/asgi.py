"""
ASGI config for candlechat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from chat.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candlechat.settings')

asgi_for_django = get_asgi_application()

application = ProtocolTypeRouter({
    'http': asgi_for_django,
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns),
    ),
})
