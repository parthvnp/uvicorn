import asyncio
import websockets


async def stt_client():
    async with websockets.connect('ws://localhost:8082/ws') as websocket:
        # Send a sample message
        await websocket.send("Hell world!")
        response = await websocket.recv()
        await websocket.close(1000)
        # Receive and print the response
        print(f"Server replied: {response}")


# Run
asyncio.run(stt_client())
