import socket
import threading
import datetime

HEADER = 64
PORT = 5050  # Figure out more about port configurations
# SERVER = "169.231.16.166"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"

# created a socket with type INET or IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected")

    connected = True
    while connected:
        connection.send(str(datetime.datetime.now()).encode(FORMAT))
        '''
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{address}] {msg}")
            connection.send("Message Received".encode(FORMAT))'''

    connection.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        print(f"[ACTIVE CONNECTION] Connected to {address}")
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting")
start()
