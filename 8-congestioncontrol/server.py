import socket
import random

def handle(c):
    name = c.recv(1024).decode()
    cwnd = 1
    ssthresh = 8

    for i in range(10):
        if random.random() < 0.2:
            if name == "Reno":
                ssthresh = max(1, cwnd / 2)
                cwnd = 1
            elif name == "CUBIC":
                cwnd = max(1, cwnd * 0.7)
            print("Loss:", round(cwnd, 2))
        else:
            if name == "Reno":
                if cwnd < ssthresh:
                    cwnd *= 2
                else:
                    cwnd += 1
            elif name == "CUBIC":
                cwnd += 2
            else:
                cwnd = 25
            print("ACK:", round(cwnd, 2))

        c.send(str(round(cwnd, 2)).encode())
        c.recv(1024)

    c.close()

s = socket.socket()
s.bind(("localhost", 5000))
s.listen()

while True:
    c, addr = s.accept()
    handle(c)