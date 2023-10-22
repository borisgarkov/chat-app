from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.connections: dict[int, WebSocket] = {}

    def add_connection(self, user_id: int, websocket: WebSocket) -> None:
        self.connections[user_id] = websocket

    async def broadcast(self, data: str) -> None:
        for connection in self.connections:
            await connection.send_text(data)

    async def send_private_message(self, recipient_id: int, message: str):
        for id_, connection in self.connections.items():
            if id_ == recipient_id:
                await connection.send_text(message)

    async def disconnect(self, user_id: int) -> None:
        print(f'{user_id} - client left chat')
        print(len(self.connections))
        # await self.connections[user_id].close()
        del self.connections[user_id]
        print(len(self.connections))
