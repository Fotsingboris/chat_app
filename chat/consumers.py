import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import Q

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.receiver_id = self.scope['url_route']['kwargs']['receiver_id']
        # Create a symmetric room name by sorting user IDs
        user_ids = sorted([str(self.user.id), str(self.receiver_id)])
        self.room_name = f"chat_{user_ids[0]}_{user_ids[1]}"

        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

        # Fetch and send old messages
        messages = await self.get_old_messages(self.user.id, self.receiver_id)
        for message in messages:
            await self.send(text_data=json.dumps({
                'message': message['content'],
                'sender': message['sender'],
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data['receiver_id']
        receiver = await self.get_receiver(receiver_id)
        sender = self.scope['user']

        await self.save_message(sender, receiver, message)

        # Use the same symmetric room name
        user_ids = sorted([str(sender.id), str(receiver.id)])
        room_name = f"chat_{user_ids[0]}_{user_ids[1]}"
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    # Rest of the methods remain unchanged
    # Sync methods for database operations
    @database_sync_to_async
    def get_receiver(self, receiver_id):
        from django.contrib.auth.models import User
        return User.objects.get(id=receiver_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        from .models import Message  # Delay import to avoid premature loading
        msg = Message(sender=sender, receiver=receiver, content=message)
        msg.save()

    @database_sync_to_async
    def get_old_messages(self, sender_id, receiver_id):
        from .models import Message  # Delay import to avoid premature loading
        # Fetch messages between the two users and order them by timestamp
        messages = Message.objects.filter(
            (Q(sender_id=sender_id) & Q(receiver_id=receiver_id)) |
            (Q(sender_id=receiver_id) & Q(receiver_id=sender_id))
        ).order_by('timestamp')

        return [{'sender': msg.sender.username, 'content': msg.content} for msg in messages]
