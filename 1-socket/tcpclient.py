import socket

s = socket.socket()
s.connect(('localhost',5001))
while True:
    msg = input("Enter message - ")
    s.send(msg.encode())
    if msg.lower() == 'exit':
        break
    print("Server : ",s.recv(1024).decode())
s.close()




