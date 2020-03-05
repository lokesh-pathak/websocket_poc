# Web Socket POC

#### reference git hub url: 
https://github.com/andrewgodwin/channels-examples/tree/master/multichat/chat 

#### Basic Explanation:
https://blog.heroku.com/in_deep_with_django_channels_the_future_of_real_time_apps_in_django

https://gearheart.io/blog/creating-a-chat-with-django-channels/

#### Django Structure
![alt text] (https://heroku-blog-files.s3.amazonaws.com/posts/1473343845-django-asgi-websockets.png)

#### Django with Channels
![alt text] (https://heroku-blog-files.s3.amazonaws.com/posts/1473343845-django-wsgi.png)

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
