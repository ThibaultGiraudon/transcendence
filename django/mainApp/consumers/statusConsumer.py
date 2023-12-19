from    channels.generic.websocket import AsyncWebsocketConsumer
import  json

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'status'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json['status']
        username = text_data_json['username']

        # Send status to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'status_update',
                'username': username,
                'id': 'id',
                'status': status
            }
        )
    
    async def status_update(self, event):
        status = event['status']
        username = event['username']
        id = event['id']

        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'username': username,
            'id': id,
            'status': status,
        }))