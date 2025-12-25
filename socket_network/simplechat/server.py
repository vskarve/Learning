import socket
import threading

DISCONNECT_MSG_CLIENT = "!CLIENT_DISCONNECT"
DISCONNECT_MSG_SERVER = "!SERVER_DISCONNECT"
HEADER = 10

class Client:

    def __init__(self, server, conn, addr):
        
        self.server_object = server
        self.connection_socket_object = conn
        self.ADDRESS = addr
        self.NAME = conn

    def communicate_with_client(self):
        print(f"[NEW CONNECTION] {self.connection_socket_object} connected.")
        connected = True

        while connected:
            message_recived = self.recive()
            self.server_socket.broadcast(self, message_recived)

        self.connection_socket_object.close()
        print(f"[TERMINATED CONNECTION] {self.connection_socket_object} disconnected.")

    def send(self, message_send, sender_name):
        encoded_message = f"[{sender_name}] {message_send}".encode(self.server_object.FORMAT)
        encoded_message_length = f"{len(encoded_message):<{self.server_object.HEADER}}".encode(self.server_object.FORMAT)
        full_message = encoded_message_length + encoded_message
        self.connection_socket_object.send(full_message)

    def recive(self):
        encoded_header = self.connection_socket_object.recv(self.server_object.HEADER)
        message_length = int(encoded_header.decode(self.server_object.FORMAT).strip())

        encoded_message = self.connection_socket_object.recv(message_length)
        return encoded_message.decode(self.server_object.FORMAT)

    def __eq__(self, other):
        '''Two client objects are the same if they have the same connection socket'''
        return self.connection_socket_object == other.connection_socket_object


class Server:
    '''Server class object'''

    def __init__(self, header=10, format="utf-8"):
        '''Header size of messages and encoding format'''
        self.SERVER_NAME = socket.gethostname() + ".local"
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.HEADER = header
        self.ADDR_PORT = self.set_and_bind_addr_port()
        self.FORMAT = format
        self.DISCONNECT_MSG_CLIENT = DISCONNECT_MSG_CLIENT
        self.DISCONNECT_MSG_SERVER = DISCONNECT_MSG_SERVER

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
        print(f"[LISTENING] Server is listening on {self.ADDR_PORT}")

        while True:
            conn, addr = self.server_socket.accept()
            client = Client(self, conn, addr)
            thread = threading.Thread(target=client.communicate_with_client)
            self.client_objects.append(client)

            thread.start()

    def broadcast(self, client_object, client_message):
        sending_client = client_object
        message = client_message

        for client in self.client_objects:
            if not client == sending_client:
                client.send(message, sending_client.name)



def main():
    server = Server()
    try:
        server.server_loop()
    finally:
        server.__del__()

if __name__ == "__main__":
    main()