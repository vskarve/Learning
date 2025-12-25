import socket

PORT = 5053
HEADER = 10
FORMAT = "utf-8"
SERVER = "172.29.198.79"
ADDR = (SERVER, PORT)
DISCONNECT_MSG_CLIENT = "!CLIENT_DISCONNECT"
DISCONNECT_MSG_SERVER = "!SERVER_DISCONNECT"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    #Formats into utf-8 format with bites
    encoded_message = msg.encode(FORMAT)
    encoded_message_length = f"{len(encoded_message):<{HEADER}}".encode(FORMAT)
    full_message = encoded_message_length + encoded_message
    client.send(full_message)

def recive():
    encoded_header = client.recv(HEADER)
    message_length = int(encoded_header.decode(FORMAT).strip())
    encoded_message = client.recv(message_length)
    return encoded_message.decode(FORMAT)

while True:
    msg = input()
    if not msg:
        continue
    send(msg)
    print(recive())
    print("NEW EPOCH")

