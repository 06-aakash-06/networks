import socket

lost = set(map(int, input("Frames to lose once: ").split()))
acklost = set(map(int, input("ACKs to lose once: ").split()))

dropped = set()
skipped = set()
expected = 0

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost", 5004))
s.listen(1)

c, addr = s.accept()
f = c.makefile("r")

while True:
    msg = f.readline().strip()

    if not msg or msg == "END":
        break

    frame = int(msg)

    if frame in lost and frame not in dropped:
        dropped.add(frame)
        print("Lost:", frame)

    elif frame == expected:
        print("Received:", frame)
        expected += 1

    else:
        print("Discarded:", frame)

    if expected in acklost and expected not in skipped:
        skipped.add(expected)
        print("Lost ACK:", expected)
    else:
        c.sendall((str(expected) + "\n").encode())
        print("ACK:", expected)

c.close()
s.close()