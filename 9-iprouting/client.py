import socket

s = socket.socket()
s.connect(("localhost", 5000))

src = input("Source PC: ")
dst = input("Destination PC: ")

s.send((src + "," + dst).encode())

print("Route:", s.recv(1024).decode())

s.close()