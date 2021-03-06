# Web Socket POC
##Websocket Definition:
```
The WebSocket Protocol enables two-way communication between a client
running untrusted code in a controlled environment to a remote host
that has opted-in to communications from that code.  The security
model used for this is the origin-based security model commonly used
by web browsers.  The protocol consists of an opening handshake
followed by basic message framing, layered over TCP.  The goal of
this technology is to provide a mechanism for browser-based
applications that need two-way communication with servers that does
not rely on opening multiple HTTP connections (e.g., using
XMLHttpRequest or <iframe>s and long polling).
```
#### reference git hub url: 
https://github.com/andrewgodwin/channels-examples/tree/master/multichat/chat 

#### Basic Explanation:
https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django

https://gearheart.io/blog/creating-a-chat-with-django-channels/

#### Django Structure
<img src="https://heroku-blog-files.s3.amazonaws.com/posts/1473343845-django-asgi-websockets.png" width="450">

#### Django with Channels
<img src="https://heroku-blog-files.s3.amazonaws.com/posts/1473343845-django-wsgi.png" width="450">

##Modify setting file
### Add channel layer definition
```
# http://channels.readthedocs.org/en/latest/deploying.html#setting-up-a-channel-backend
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('*', 6379)],
        },
    },
}
```

#### ADD channel in install app
```
INSTALLED_APPS = [
'channels',
]
```
#### ASGI_APPLICATION
```
ASGI_APPLICATION = "websocket_poc.routing.application"
```

###Create Routing file:
```
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from chat import routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
```

###Create Consumer:
```
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
``` 

#### Hit Socket via extension
```
url:- ws://127.0.0.1:8000/chat/1/
{"command":"get_room_messages","message":"Hello"}
```

#### Hit socket via browser
```
http://127.0.0.1:8000/chat/

then create room say, lobby

http://127.0.0.1:8000/chat/lobby/

open same url in two diffrent browser i.e in same room now you can broadcast to that room.
```