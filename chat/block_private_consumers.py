import json

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from .models import PrivateBlock


class PrivateBlockConsumer(WebsocketConsumer):
    def connect(self):
        present_user = self.scope['user'].id if self.scope['user'].id else int(self.scope['query_string'])
        other_user = self.scope['url_route']['kwargs']['userId']
        self.private_block_name = (
            f'{present_user}_{other_user}'
            if int(present_user) > int(other_user)
            else f'{other_user}_{present_user}'
        )
        self.private_block_chat_name = f'block_{self.private_block_name}'
        self.user = self.scope['user']

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.private_block_chat_name,
            self.channel_name
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.private_block_chat_name,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if not self.user.is_authenticated:
            return

        async_to_sync(self.channel_layer.group_send)(
            self.private_block_chat_name,
            {
                'type': 'private_block_message',
                'user_id': self.user.id,
                'user': self.user.username,
                'message': message
            }
        )
        PrivateBlock.objects.create(
            user=self.user,
            message=message,
            block_thread=self.private_block_chat_name
        )

    def private_block_message(self, event):
        self.send(text_data=json.dumps(event))
