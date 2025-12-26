import socket

PORT = 5052
HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.29.198.79"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    #Formats into utf-8 format with bites
    message = msg.encode(FORMAT)
    #since server needs to know msg length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    #first message neeads to have size if HEADER (hard coded on server), b" " is a byte literal of value 0x20 and only occupies one bite
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

print(ADDR)
while True:
    msg = input()
    if not msg:
        send(DISCONNECT_MESSAGE)
        break
    send(msg)
    