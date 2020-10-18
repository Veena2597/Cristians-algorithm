import socket
import datetime
import time
from dateutil import parser
from timeit import default_timer
import threading
import logging
import sys

HEADER = 64
PORT = 5052  # Figure out more about port configurations
# SERVER = "169.231.16.166"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"
CLOCK_REQUEST = "SYNCHRONIZE"
CLIENTS_LIST = {'CLIENT1': 5051, 'CLIENT2': 5052, 'CLIENT3': 5053}

logging.basicConfig(filename='client2.log', level=logging.DEBUG)

bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bind_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

class Node:
    def __init__(self, timestamp, amount, sender, receiver):
        self.amount = amount
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp
        self.next = None


class Blockchain:
    def _init_(self):
        self.head = None


def clientClock(clock_server_time, delay):
    current_sys_time = datetime.datetime.now()
    sys_time_at_sync = clock_server_time
    sim_time_at_sync = clock_server_time + datetime.timedelta(seconds=(delay) / 2)
    current_sim_time = sim_time_at_sync + current_sys_time - sys_time_at_sync
    return current_sim_time


def synchronizeTime():
    # Client sends CLOCK_REQUEST to the clock server and the request time is recorded
    request_time = default_timer()
    connect_socket.send(CLOCK_REQUEST.encode(FORMAT))
    logging.debug("[CLOCK SERVER] Requested time from server at {}".format(request_time))

    # Client receives time from the clock server and the response time is recorded
    clock_server_time = parser.parse(connect_socket.recv(1024).decode(FORMAT))
    response_time = default_timer()
    actual_time = datetime.datetime.now()
    logging.debug("[CLOCK SERVER] Time received from clock server {}".format(str(clock_server_time)))

    # Delay between request sent and response received is calculated
    delay = response_time - request_time
    logging.debug("[CLIENT CLOCK] Delay in response from clock server is {}s".format(str(delay)))

    # Times before and after synchronization are printed
    logging.debug("[CLIENT CLOCK] Time before synchronization {}s".format(str(actual_time)))
    client_time = clock_server_time + datetime.timedelta(seconds=(delay) / 2)  # Calculated with Cristian's algorithm
    logging.debug("[CLIENT CLOCK] Time after synchronization {}s".format(str(client_time)))

    error = actual_time - client_time
    logging.debug("[CLIENT CLOCK] Synchronization error {}s".format(str(error.total_seconds())))

    # The client ping the clock again after 20s
    time.sleep(10)


if __name__ == '__main__':
    bind_socket.bind(ADDRESS)
    bind_socket.listen()

    while True:
        connect_socket.connect_ex((SERVER, 5053))
        connect_socket.connect_ex((SERVER, 5051))
        connect_socket.connect_ex((SERVER, 5050))
        connection, address = bind_socket.accept()
        print(connection)
        clock_thread = threading.Thread(target=synchronizeTime)
        clock_thread.start()
        #clients_thread = threading.Thread(target=updateClients)
        #clients_thread.start()
        '''raw = input("Enter transaction:")
        print(raw + "\n")
        msg = client.recv(1024).decode(FORMAT)
        print(msg)'''
    client.close()
