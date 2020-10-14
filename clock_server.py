import socket
import datetime
import threading

PORT = 5050  # Figure out more about port configurations
# SERVER = "169.231.16.166"
CLOCK_SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (CLOCK_SERVER, PORT)
FORMAT = 'utf-8'
CLOCK_REQUEST = "SYNCHRONIZE"


def sendTime():
    connected = True
    while connected:
        msg = connection.recv(1024).decode(FORMAT)
        if msg == CLOCK_REQUEST:
            connection.send(str(datetime.datetime.now()).encode(FORMAT))
    connection.close()


if __name__ == '__main__':
    clock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("f[CLOCK] Successfully created")
    clock.bind(ADDRESS)

    clock.listen()
    print("f[CLOCK LISTEN] Clock server is listening")

    while True:
        connection, address = clock.accept()
        print(f"[NEW CONNECTION] {address} connected")
        thread = threading.Thread(target=sendTime(), args=(connection, address))
        thread.start()

    clock.close()