import socket

n = int(input("Number of frames: "))
w = int(input("Window size: "))

s = socket.socket()
s.connect(("localhost", 5004))
s.settimeout(2)

base = 0
received = b""

while base < n:
    end = min(base + w, n)

    for i in range(base, end):
        s.sendall((str(i) + "\n").encode())
        print("Sent:", i)

    try:
        while base < end:
            while b"\n" not in received:
                received += s.recv(1024)

            line, received = received.split(b"\n", 1)
            ack = int(line)

            print("ACK:", ack)
            base = max(base, ack)

    except socket.timeout:
        print("Timeout, retransmitting")

s.sendall(b"END\n")
s.close()