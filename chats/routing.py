# 라우팅 설정을 통해 컨슈머와 URL을 연결합니다.

from django.urls import path, re_path
from . import consumers

websocket_urlpatterns = [
    path("ws/chats/<int:room_pk>", consumers.RolePlayingRoomConsumer.as_asgi()),
<<<<<<< HEAD
    path("ws/connect_path/", consumers.MyConsumer.as_asgi()),
=======
>>>>>>> 511da81 (websocket연결중_ path변경 및 cors추가)
]
