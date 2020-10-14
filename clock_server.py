import socket
import datetime


PORT = 5050  # Figure out more about port configurations
# SERVER = "169.231.16.166"
CLOCK_SERVER = ''
ADDRESS = (CLOCK_SERVER, PORT)
FORMAT = 'utf-8'


def initClockServer():
    clock = socket.socket()
    print("f[CLOCK] Successfully created")

    clock.listen()
    print("f[CLOCK LISTEN] Clock server is listening")

    while True:
        connection, address = clock.accept()
        connection.send(str(datetime.datetime.now()).encode(FORMAT))
        connection.close()

if __name__ == '__main__':
    initClockServer()