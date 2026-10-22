import socket

#gobacknserver
lost = set()
for x in input("Frames to lose: ").split():
    lost.add(int(x))
acklost = set()
for x in input("ACKs to lose: ").split():
    acklost.add(int(x))
expected = 0
s = socket.socket()
s.bind(("localhost", 5004))
s.listen(1)
c, addr = s.accept()
buffer = ""
while True:
    buffer += c.recv(1024).decode()
    while "\n" in buffer:
        msg, buffer = buffer.split("\n", 1)
        if msg == "END":
            c.close()
            s.close()
            quit()
        frame = int(msg)
        if frame in lost:
            print("Lost:", frame)
            lost.remove(frame)
        elif frame == expected:
            print("Received:", frame)
            expected += 1
        else:
            print("Discarded:", frame)
        if expected in acklost:
            print("Lost ACK:", expected)
            acklost.remove(expected)
        else:
            c.sendall((str(expected) + "\n").encode())
            print("ACK:", expected)
            