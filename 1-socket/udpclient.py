import socket

#udpclient
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    msg = input("Enter message - ")
    if msg.lower() == 'exit':
        break
    s.sendto(msg.encode(), ('localhost', 5001))
    data, addr = s.recvfrom(1024)
    print("Server:", data.decode())
s.close()



