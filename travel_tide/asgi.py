# travel_tide/asgi.py
import os
import django

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.routing import ProtocolTypeRouter, URLRouter
from chatserver.routing import websocket_urlpatterns  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_tide.settings')
django.setup()

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": (
            (URLRouter(websocket_urlpatterns))
        ),
    }
)