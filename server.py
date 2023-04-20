import asyncio
import websockets
import socket

# List to keep track of connected clients
clients = []

async def handle_websocket(websocket, path):
    # Add client to the list of connected clients
    clients.append(websocket)

    try:
        # Wait for the client to send their chosen username
        username = await websocket.recv()
        client_name = username.strip()

        # Send a message to all connected clients announcing the new client
        join_message = f"[SERVER] - {client_name} has joined the chat"
        for client in clients:
            await client.send(join_message)

        # Keep the connection open and handle incoming messages
        async for message in websocket:
            print(f"[+] Received message from client [{client_name}]: {message}")
            # Send the message to all connected clients, excluding the sender
            for client in clients:
                if client != websocket:
                    await client.send(f"[{client_name}]: {message}")
    finally:
        # Remove the client from the list of connected clients when the connection is closed
        clients.remove(websocket)
        # Send a message to all connected clients announcing that the client has left the chat
        leave_message = f"[SERVER] - {client_name} has left the chat"
        for client in clients:
            await client.send(leave_message)


async def main():
    # Get the server IP address
    server_ip = socket.gethostbyname(socket.gethostname())
    print(f"Server running at ws://{server_ip}:8765")

    # Start the WebSocket server
    async with websockets.serve(handle_websocket, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())