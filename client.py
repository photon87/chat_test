import sys
import time
import socket
from net import Network
from message import Message

ip = input("Server: ")
if ip == "":
    ip = socket.gethostbyname(socket.gethostname())

name = input("Username: ")
DISCONNECT_MESSAGE = "!DISCONNECT"

n = Network(ip)
first = Message(name, "test", "default", time.time())
n.connect(first)

def send_msg(msg):
        m = Message(name, str(msg), "default", time.time())
        return n.send(m)

def main():
    while True:
        send_msg(str(input()))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        send_msg(DISCONNECT_MESSAGE)
        n.disconnect()
        sys.exit(0)