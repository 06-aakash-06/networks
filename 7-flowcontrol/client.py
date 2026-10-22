import socket

s = socket.socket()
s.connect(("localhost", 5000))
f = s.makefile("r")

n = int(input("Number of segments: "))
window = int(f.readline())
sent = 0

while sent < n:
    count = min(window, n - sent)

    s.sendall((str(count) + "\n").encode())
    print("Sent:", count, "segments")

    sent += count
    window = int(f.readline())

    print("Receiver window:", window)

s.sendall(b"END\n")
s.close()