import socket
import threading

class Client:

    def __init__(self):
        self.connection_socket_object = None
        self.name = None


class Server:
    '''Server class object'''

    def __init__(self, header=10, format="utf-8"):
        '''Header size of messages and encoding format'''
        self.SERVER_NAME = socket.gethostname() + ".local"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.HEADER = header
        self.ADDR_PORT = self.set_and_bind_addr_port()
        self.FORMAT = format
        self.DISCONNECT_MSG = "!DISCONNECT"

        self.client_objects = []

    def __del__(self):
        '''Closes the socket object'''
        self.server_socket.close()

    def set_and_bind_addr_port(self, start_port=5050):
        '''Tests valid ports starting with start_port. Binds and returns servers address and port'''
        port = start_port
        addr = socket.gethostbyname(self.SERVER_NAME)
        while True:
            try:
                self.server_socket.bind((addr, port))
                return (addr, port)
            except OSError:
                port += 1

    def server_loop(self, max_queue_length=socket.SOMAXCONN):
        '''Maxiumum length of listening queue. Server loop that handle and connects clients'''
        self.server_socket.listen(max_queue_length)

def main():
    server = Server()
    server.server_loop()

if __name__ == "__main__":
    main()