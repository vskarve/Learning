import socket
import threading

PORT = 5050

#Ipv4 adress (local adress on router system, wont be reachable outside router)
#SERVER = "172.29.198.79" (an example, but to get for every computer run below)
#To get the local on router add "local" otherwise it will give you a adres on local on the computer (127...)
SERVER = socket.gethostbyname(socket.gethostname() + ".local")
print(SERVER)
print(socket.gethostname())