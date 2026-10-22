import socket

s = socket.socket()
s.connect(("localhost", 5000))

name = input("Reno / CUBIC / BBR: ")
s.send(name.encode())

for i in range(10):
    cwnd = s.recv(1024).decode()
    print("Round", i + 1, "cwnd:", cwnd)
    s.send(b"ACK")

s.close()