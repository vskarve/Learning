import socket
import threading
import time

#/Desktop/Learning/socket_network/localtest1

PORT = 5051
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

#Ipv4 adress (local adress on router system, wont be reachable outside router)
#SERVER = "172.29.198.79" (an example, but to get for every computer run below)
#To get the local on router add "local" otherwise it will give you a adres on local on the computer (127...)
SERVER = socket.gethostbyname(socket.gethostname() + ".local")

#adress abbriviation
ADDR = (SERVER, PORT)

#Use Ipv4 (familty) and stream (type) the data (mainly that it is TCP, where as DGRAM is UDP)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {conn} connected.")

    connected = True
    while connected:
        #How many bites do we want to recive
        #Pauses until message recived, hence threading
        msg_length = conn.recv(HEADER).decode(FORMAT)

        #When connecting a empy string is sent as message (only once), which is invalid for the program below
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{addr}] {msg}")
            conn.send("MSG_recived".encode(FORMAT))

    conn.close()

def start():
    #Set the server to listening mode, making a queue of incoming requests
    #Can set queue size
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        #accepts one connection request, conn is a socket object
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        #-1 since the staring thread is counted for
        print(f"[ACTIVE CONNECTINS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()