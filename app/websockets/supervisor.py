from fastapi import WebSocket

async def supervisor_socket(ws: WebSocket):
    await ws.accept()
    while True:
        await ws.send_json({"event":"heartbeat"})