from django.conf.urls import url
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatTestConsumer),
    url(r'^chat/(?P<group_id>[^/]+)/$', consumers.ChatConsumer),
]
