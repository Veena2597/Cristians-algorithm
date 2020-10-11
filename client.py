import socket

HEADER = 64
PORT = 5050  # Figure out more about port configurations
# SERVER = "169.231.16.166"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(message):
    msg = message.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(msg)
    print(client.recv(2048).decode(FORMAT))


send("Connection Secure")
send(DISCONNECT_MESSAGE)
