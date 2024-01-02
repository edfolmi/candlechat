import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import Block, GroupBlock


class GroupBlockConsumer(WebsocketConsumer):
    def connect(self):
        self.block_slug = self.scope['url_route']['kwargs']['slug']
        self.group_block_name = f'block_{self.block_slug}'
        self.block = Block.objects.get(slug=self.block_slug)
        self.user = self.scope['user']

        self.accept()

        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.block.online.all()],
        }))

        async_to_sync(self.channel_layer.group_add)(
            self.group_block_name,
            self.channel_name
        )

        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                self.group_block_name,
                {
                    'type': 'user_connect',
                    'user': self.user.username
                }
            )
            self.block.online.add(self.user)

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_block_name,
            self.channel_name
        )
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_send)(
                self.group_block_name,
                {
                    'type': 'user_disconnect',
                    'user': self.user.username
                }
            )
            self.block.online.remove(self.user)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        async_to_sync(self.channel_layer.group_send)(
            self.group_block_name,
            {
                'type': 'block_message',
                'user_id': self.user.id,
                'user': self.user.username,
                'message': message
            }
        )
        GroupBlock.objects.create(
            user=self.user,
            block=self.block,
            content=message
        )

    def block_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_connect(self, event):
        self.send(text_data=json.dumps(event))

    def user_disconnect(self, event):
        self.send(text_data=json.dumps(event))
