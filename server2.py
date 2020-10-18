import socket
import threading
import pickle
import time
from message import Message


class Server():
    def __init__(self):
        self.HEADER = 64
        self.PORT = 9001
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.TIME_FORMAT = '%b %d %Y %H:%M:%S'

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.last_msg = None

    def send(self, msg, conn, addr, pick=True,):
        if pick:
            message = pickle.dumps(msg)
        else:
            message = msg
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length)
                msg = pickle.loads(msg)
                if msg.get_message() == self.DISCONNECT_MESSAGE:
                    connected = False

                #t = time.strftime(self.TIME_FORMAT, time.localtime(msg.get_time()))
                #print(f"[{t}] {msg.get_client_name()}: {msg.get_message()}")

                self.last_msg = msg
                t = time.strftime(
                    self.TIME_FORMAT, time.localtime(self.last_msg.get_time()))
                response = Message(
                    "SERVER", f"last_msg received @ {t}", "default", time.time())
                self.send(response, conn, addr)
                time.sleep(0.001)
        conn.close()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(
                target=self.handle_client, args=(conn, addr))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == "__main__":

    print("[STARTING] Server is starting...")
    s = Server()

    s.start()
