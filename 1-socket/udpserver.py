import socket
import threading

#udpserver
def handle(data, addr):
    print(addr, "Client:", data.decode())
    s.sendto(data, addr)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 5001))
print("UDP Server waiting...")
while True:
    data, addr = s.recvfrom(1024)
    threading.Thread(target=handle, args=(data, addr)).start()
    
    
    
    