import socket
import datetime
import time
from dateutil import parser
from timeit import default_timer
import threading
import logging
import pickle
import sys

HEADER = 64
PORT = 5053  # Figure out more about port configurations
# SERVER = "169.231.16.166"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECTED"
CLOCK_REQUEST = "SYNCHRONIZE"
CLIENTS_LIST = {'CLIENT1': 5051, 'CLIENT2': 5052, 'CLIENT3': 5053}


logging.basicConfig(filename='client1.log', level=logging.DEBUG)
clock_server_time = 0
client_time_at_sync = 0
client_sockets = []
bind_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bind_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clock_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


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

    def push(self, timestamp, amount, sender, receiver):
        node = Node(timestamp, amount, sender, receiver)
        if self.head is None:
            self.head = node
            return

        last = self.head
        while last.next:
            last = last.next
        last.next = node

    def traverse(self):
        temp = self.head
        balance = 10
        validity = 1
        while temp:
            if temp.sender == 'B':
                balance = balance - temp.amount
            elif temp.receiver == 'B':
                balance = balance + temp.amount
            temp = temp.next
        if balance < 0:
            validity = 0
        return validity, balance

def clientClock(clock_server_time, delay):
    current_sys_time = datetime.datetime.now()
    sys_time_at_sync = clock_server_time
    sim_time_at_sync = clock_server_time + datetime.timedelta(seconds=(delay) / 2)
    current_sim_time = sim_time_at_sync + current_sys_time - sys_time_at_sync
    return current_sim_time


def synchronizeTime():
    # Client sends CLOCK_REQUEST to the clock server and the request time is recorded
    while True:
        request_time = default_timer()
        clock_socket.send(CLOCK_REQUEST.encode(FORMAT))
        logging.debug("[CLOCK SERVER] Requested time from server at {}".format(request_time))

        # Client receives time from the clock server and the response time is recorded
        clock_server_time = parser.parse(clock_socket.recv(1024).decode(FORMAT))
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
        time.sleep(20)


def listenTransaction():
    # connection.recv, update the local buffer
    pass


def broadcastTransaction():
    pass


def inputTransactions(client_socks):
    global client_time_at_sync
    global client_sockets
    global buffer

    block = Blockchain()
    print(block.head)
    while True:
        raw_type = input("Please enter your transaction:")
        s = raw_type.split(' ')
        print(s)

        if s[0] == 'T':
            timestamp = clientClock()
            print(timestamp)
            tran = {'sender': s[1], 'receiver': s[2], 'amount': s[3], 'timestamp': timestamp}
            b = pickle.dumps(tran)
            heappush(buffer, Node(timestamp, s[3], s[1], s[2]))
            print(buffer)

            for sock in range(len(client_sockets)):
                sock.send(bytes(b))

            time.sleep(2)
            while len(buffer) > 0:
                y = heappop(buffer)
                block.push(y)

            validity, balance = block.traverse()
            print(validity, balance)
            print(client_time_at_sync)
            # update blockchain and traverse it till the current node. Check amount and validity of transaction
        elif s[0] == 'b':
            pass


if __name__ == '__main__':
    block = Blockchain()
    bind_socket.bind(ADDRESS)
    bind_socket.listen()
    clock_socket.connect((SERVER, 5050))
    client_sockets = []
    for i in range(1, 4):
        if i != 3:
            connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            connect_socket.connect_ex((SERVER, 5050 + i))
            client_sockets.append(connect_socket)

    clock_thread = threading.Thread(target=synchronizeTime)
    clock_thread.start()
    my_transactions = threading.Thread(target=inputTransactions, args=client_sockets)
    my_transactions.start()
    while True:
        connection, address = bind_socket.accept()
        logging.debug("[CLIENT CONNECTED] {}".format(str(connection)))
        print(connection)

        listen_transactions = threading.Thread(target=listenTransaction, args=connection)
        listen_transactions.start()
        '''
        broadcast_transaction = threading.Thread(target=broadcastTransaction, args=connection)
        broadcast_transaction.start()'''
    clock_socket.close()
    bind_socket.close()
