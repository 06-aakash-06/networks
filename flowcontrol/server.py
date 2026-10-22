import socket
import time

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 5000))
s.listen(1)

c, addr = s.accept()
f = c.makefile("r")

capacity = 4
buffer = 0
received = 0

c.sendall(b"4\n")

while True:
    msg = f.readline().strip()

    if not msg or msg == "END":
        break

    n = int(msg)
    buffer += n
    received += n

    print("Buffer occupied:", buffer)

    time.sleep(0.5)

    buffer -= min(1, buffer)

    window = capacity - buffer

    print("Receiver window:", window)
    c.sendall((str(window) + "\n").encode())

print("Total received:", received)

c.close()
s.close()