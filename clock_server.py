import socket
import datetime
import threading

PORT = 5050  # Figure out more about port configurations
# SERVER = "169.231.16.166"
CLOCK_SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (CLOCK_SERVER, PORT)
FORMAT = 'utf-8'
CLOCK_REQUEST = "SYNCHRONIZE"


def sendTime(connection, address):
    connected = True
    while connected:
        # Client sends CLOCK_REQUEST whenever it needs to know the time from the server
        msg = connection.recv(1024).decode(FORMAT)
        if msg == CLOCK_REQUEST:
            connection.send(str(datetime.datetime.now()).encode(FORMAT))

    connection.close()


if __name__ == '__main__':
    # Creating the clock server socket
    clock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("f[CLOCK SERVER] Successfully created")

    # Binding the clock server socket to the address - defined globally
    clock.bind(ADDRESS)

    # The clock server keeps listening for different clients
    clock.listen()
    print("f[CLOCK SERVER] Clock server is listening")

    while True:
        # Clock server accepts new clients and creates a new thread for each client
        connection, address = clock.accept()
        print(f"[CLOCK SERVER]  New client connected with address: {address}")
        thread = threading.Thread(target=sendTime, args=(connection, address))
        thread.start()
        print(f"[CLOCK SERVER] Current number of clients connected: {threading.active_count() - 1}")

    clock.close()
