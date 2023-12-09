# travel_tide/asgi.py
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chatserver.routing  # Import your routing configuration
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_tide.settings')
 
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chatserver.routing.websocket_urlpatterns  # Adjust this based on your routing configuration
            )
        ),
    }
)
