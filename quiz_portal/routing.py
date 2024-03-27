from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from quizzes import consumers

# urls that handles the websocket connection is put here
websocket_urlpatterns=[
                    re_path(
                        r"ws/game/(?P<game_id>\w+)/$", consumers.GameConsumer.as_asgi()
                    ),
                ]

application = ProtocolTypeRouter( 
    {
        "websocket": AuthMiddlewareStack(
            URLRouter(
               websocket_urlpatterns
            )
        ),
    }
)
