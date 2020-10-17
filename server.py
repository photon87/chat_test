import socket
import threading
import pickle
from message import Message
import time

HEADER = 64
PORT = 9001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
TIME_FORMAT = '%b %d %Y %H:%M:%S'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    def send(msg, pick=True):
        if pick:
            message = pickle.dumps(msg)
        else:
            message = msg
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length)
            msg = pickle.loads(msg)
            if msg.get_message() == DISCONNECT_MESSAGE:
                connected = False

            if msg.get_message_type() == "default":
                t = time.strftime(TIME_FORMAT, time.localtime(msg.get_time()))
                print(f"[{t}] {msg.get_client_name()}: {msg.get_message()}")
            elif msg.get_message_type() == "player":
                pass
            last_msg = msg
            t = time.strftime(TIME_FORMAT, time.localtime(last_msg.get_time()))
            response = Message(
                "SERVER", f"last_msg received @ {t}", "default", time.time())
            send(response)
            time.sleep(0.015)
    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] Server is starting...")
start()
