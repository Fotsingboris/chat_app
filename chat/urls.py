from os import path
from django.urls import re_path

from chat.views import get_chat_messages
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
    
        path('get_messages/<int:receiver_id>/', get_chat_messages, name='get_chat_messages'),
        

]