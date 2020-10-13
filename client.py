import socket
import datetime
from dateutil import parser
from timeit import default_timer

HEADER = 64
PORT = 5050  # Figure out more about port configurations
# SERVER = "169.231.16.166"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def send(message):
    msg = message.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(msg)
    print(client.recv(2048).decode(FORMAT))


def synchronizeTime():
    request_time = default_timer()
    clock_server_time = parser.parse(client.recv(1024).decode(FORMAT))
    response_time = default_timer()
    actual_time = datetime.datetime.now()

    print(f"[CLOCK SERVER] Time from clock server {str(clock_server_time)}")

    delay = response_time - request_time
    print(f"[CLOCK DELAY] {str(delay)}s")
    print(f"[CLIENT CLOCK] Before synchronization {str(actual_time)}s")

    client_time = clock_server_time + datetime.timedelta(seconds= (delay)/2)
    print(f"[CLIENT CLOCK] After synchronization {str(client_time)}s")

    error = actual_time - client_time
    print(f"[CLIENT CLOCK] Synchronization error {str(error.total_seconds())}s")


if __name__ == '__main__':
    client.connect(ADDRESS)
    synchronizeTime()
    #send("Connection Secure")
    #send(DISCONNECT_MESSAGE)
    client.close()
