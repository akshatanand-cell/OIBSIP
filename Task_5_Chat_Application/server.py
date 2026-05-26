import socket
import threading
import datetime

# ─────────────────────────────────────────────
#  Akshat_Anand_Task5 — Chat Application Server
#  Oasis Infobyte Python Internship
# ─────────────────────────────────────────────

HOST = "127.0.0.1"
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

print(f"🚀 Server started on {HOST}:{PORT}")
print("Waiting for connections...\n")

def broadcast(message, sender=None):
    """Send message to all connected clients."""
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    """Remove a disconnected client."""
    if client in clients:
        index = clients.index(client)
        username = usernames[index]
        clients.remove(client)
        usernames.remove(username)
        client.close()
        time_str = datetime.datetime.now().strftime("%H:%M")
        msg = f"[{time_str}] ⚠️  {username} left the chat.".encode("utf-8")
        broadcast(msg)
        print(f"[-] {username} disconnected.")

def handle_client(client):
    """Handle messages from a single client."""
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message:
                index = clients.index(client)
                username = usernames[index]
                time_str = datetime.datetime.now().strftime("%H:%M")
                full_msg = f"[{time_str}] {username}: {message}"
                print(full_msg)
                broadcast(full_msg.encode("utf-8"), sender=client)
                # Echo back to sender too
                client.send(full_msg.encode("utf-8"))
        except:
            remove_client(client)
            break

def receive():
    """Accept new client connections."""
    while True:
        client, address = server.accept()
        print(f"[+] New connection from {address}")

        # Ask for username
        client.send("USERNAME".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")

        clients.append(client)
        usernames.append(username)

        time_str = datetime.datetime.now().strftime("%H:%M")
        print(f"[+] {username} joined the chat.")

        # Notify everyone
        join_msg = f"[{time_str}] 🟢 {username} joined the chat!".encode("utf-8")
        broadcast(join_msg)
        client.send(f"[{time_str}] ✅ Connected! Welcome {username}!".encode("utf-8"))

        # Start thread for this client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()

receive()
