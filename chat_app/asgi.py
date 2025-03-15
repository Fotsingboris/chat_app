import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

# Set up Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chat_app.settings")

# Define the application callable
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP requests go to the regular Django app
    "websocket": AuthMiddlewareStack(  # WebSocket requests go to the WebSocket app
        URLRouter(
            chat.routing.websocket_urlpatterns  # URL routing for WebSocket
        )
    ),
})
