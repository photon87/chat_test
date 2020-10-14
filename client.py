import time
from net import *
from message import *

name = input("Username: ")
DISCONNECT_MSG = Message(name, "!DISCONNECT", time.time())

n = Network()
first = Message(name, "test", time.time())
n.connect(first)

while True:
    m = Message(name, str(input()), time.time())
    n.send(m)
