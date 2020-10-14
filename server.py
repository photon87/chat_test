import socket
import threading
import pickle
import message
import time

HEADER = 64
PORT = 9001
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

log = []


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
            t = time.strftime('%b %d %Y %H:%M:%S',
                              time.localtime(msg.get_time()))
            print(f"[{t}] {msg.get_client_name()}: {msg.get_message()}")
            log.append(msg)
            send(log)
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
