import socket
import threading
import random
import time

busy = False
lock = threading.Lock()

def handle(c):
    global busy

    while True:
        msg = c.recv(1024).decode()

        if not msg or msg == "exit":
            break

        cw = 4

        while True:
            time.sleep(random.randint(0, cw - 1) * 0.01)

            with lock:
                if not busy:
                    busy = True
                    break

            cw = min(cw * 2, 16)
            print("Channel busy, CW:", cw)

        print("Sending:", msg)
        time.sleep(0.1)

        with lock:
            busy = False

        c.send(b"ACK")

    c.close()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 5000))
s.listen()

while True:
    c, addr = s.accept()
    threading.Thread(target=handle, args=(c,)).start()