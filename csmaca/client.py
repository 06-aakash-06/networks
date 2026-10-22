import socket

s = socket.socket()
s.connect(("localhost", 5000))

while True:
    msg = input("Enter packet: ")

    if msg == "exit":
        s.send(b"exit")
        break

    s.send(msg.encode())
    print("Server:", s.recv(1024).decode())

s.close()