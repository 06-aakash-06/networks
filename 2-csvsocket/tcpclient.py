import socket


s = socket.socket()
s.connect(("localhost", 5000))
while True:
    roll = input("Enter roll number: ")
    if roll == "exit":
        break
    s.send(roll.encode())
    print(s.recv(1024).decode())
s.close()



