from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat//(?P<conversation_id>\d+)/(?P<user_id>\d+)/$",
            consumers.ConversationConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<user_id>\d+)/",
            consumers.ConversationConsumer.as_asgi()),
]
