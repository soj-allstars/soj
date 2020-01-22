from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from problemset.urls import websocket_urlpatterns

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
})
