import logging
from typing import List

from starlette.websockets import WebSocketState, WebSocketDisconnect

import uvicorn
from fastapi import FastAPI, WebSocket

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


logger = logging.getLogger("uvicorn.error")


@app.websocket('/ws')
async def stt(ws: WebSocket):
    await manager.connect(ws)
    print("Connection accepted")
    while True:
        if ws.application_state == WebSocketState.DISCONNECTED:
            print("Connection closed")
            break
        message = await ws.receive_text()
        print(f"received message: {message}")
        await ws.send_text(f"You said: {message}")


if __name__ == '__main__':
    manager = ConnectionManager()
    uvicorn.run(app=app, port=8082, log_level="debug")
