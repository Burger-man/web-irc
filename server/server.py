import asyncio
import websockets
import socket
import json

# List to keep track of connected clients
clients = []

# Read the configuration file into a string
with open('config.json', 'r') as f:
    config_data = f.read()

# Parse the configuration data into a Python dictionary
config = json.loads(config_data)

# Access the shutdown ID from the dictionary
shutdown_id = config['shutdown_id']

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
            
            # Check if the client is attempting to shut down the server
            if message.strip() == f"kill({shutdown_id})":
                # Send a message to all connected clients announcing that the server is shutting down
                shutdown_message = f"[SERVER] - {client_name} has initiated a server shutdown"
                for client in clients:
                    await client.send(shutdown_message)
                
                # Wait for a moment to allow the message to propagate
                await asyncio.sleep(1)
                
                # Close all client connections and stop the event loop
                for client in clients:
                    await client.close()
                asyncio.get_event_loop().stop()
            
            # Otherwise, send the message to all connected clients, excluding the sender
            else:
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