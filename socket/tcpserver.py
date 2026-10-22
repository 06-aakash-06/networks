import socket
import threading

def handle(c,addr):
    print("Connected - ",addr)
    while True:
        msg = c.recv(1024).decode()
        if not msg or msg == "exit":
            break
        print(addr,"Client : ",msg)
        c.send(msg.upper().encode())
    c.close()
    
s = socket.socket()
s.bind(('localhost',5001))
s.listen(1)

while True:
    c,addr = s.accept()
    threading.Thread(target=handle,args=(c,addr)).start()