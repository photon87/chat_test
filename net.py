import socket
import pickle


class Network:
    def __init__(self, ip):
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = ip
        self.port = 9001
        self.addr = (self.host, self.port)

        self.id = None

    def connect(self, name):
        self.client.connect(self.addr)
        self.send(name)

    def disconnect(self):
        self.client.close()

    def send(self, msg, pick=True):
        if pick:
            message = pickle.dumps(msg)
        else:
            message = msg
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = self.client.recv(msg_length)
            msg = pickle.loads(msg)
        return msg
