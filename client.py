import time
import socket
from net import Network
from message import Message

ip = input("Server: ")
if ip == "":
    ip = socket.gethostbyname(socket.gethostname())

name = input("Username: ")
DISCONNECT_MSG = Message(name, "!DISCONNECT", time.time())

n = Network(ip)
first = Message(name, "test", time.time())
n.connect(first)

while True:
    m = Message(name, str(input()), time.time())
    n.send(m)
