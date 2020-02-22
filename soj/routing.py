from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from problemset.urls import websocket_urlpatterns as pwu
from contest.urls import websocket_urlpatterns as cwu

websocket_urlpatterns = pwu + cwu

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
})
