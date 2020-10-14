import socket
import datetime
import time
from dateutil import parser
from timeit import default_timer
import threading

HEADER = 64
PORT = 5050  # Figure out more about port configurations
# SERVER = "169.231.16.166"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"
CLOCK_REQUEST = "SYNCHRONIZE"
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
    # Client sends CLOCK_REQUEST to the clock server and the request time is recorded
    request_time = default_timer()
    client.send(CLOCK_REQUEST.encode(FORMAT))
    print(f"[CLOCK SERVER] Requested time from server at {request_time}")

    # Client receives time from the clock server and the response time is recorded
    clock_server_time = parser.parse(client.recv(1024).decode(FORMAT))
    response_time = default_timer()
    actual_time = datetime.datetime.now()
    print(f"[CLOCK SERVER] Time received from clock server {str(clock_server_time)}")

    # Delay between request sent and response received is calculated
    delay = response_time - request_time
    print(f"[CLIENT CLOCK] Delay in response from clock server is {str(delay)}s")

    # Times before and after synchronization are printed
    print(f"[CLIENT CLOCK] Time before synchronization {str(actual_time)}s")
    client_time = clock_server_time + datetime.timedelta(seconds= (delay)/2)  # Calculated with Cristian's algorithm
    print(f"[CLIENT CLOCK] Time after synchronization {str(client_time)}s")

    error = actual_time - client_time
    print(f"[CLIENT CLOCK] Synchronization error {str(error.total_seconds())}s")

    # The client ping the clock again after 20s
    time.sleep(20)


if __name__ == '__main__':
    client.connect(ADDRESS)
    while True:
        # Client connects to the clock server and a thread is created for synchronizing time
        clock_thread = threading.Thread(target=synchronizeTime())
        clock_thread.start()

    client.close()
