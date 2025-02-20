'''from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]'''
from django.urls import re_path
from . import consumers
from django.urls import path
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room>\w+)/$', consumers.ChatConsumer.as_asgi()),
    #path('ws/video-call/<int:video_call_id>/', consumers.CallConsumer.as_asgi()),
    #re_path(r'ws/video-call/(?P<video_call_id>\d+)/$', consumers.CallConsumer.as_asgi()),
]              #chat

