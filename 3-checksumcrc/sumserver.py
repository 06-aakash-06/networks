import socket

def checksum(data):
    total = sum(data)
    while total > 255:
        total = total % 256 + total // 256
    return 255 - total
s = socket.socket()
s.bind(("localhost", 5000))
s.listen(1)
print("Server waiting...")
while True:
    c, addr = s.accept()
    data = []
    for x in c.recv(1024).decode().split():
        data.append(int(x))
    print("Received:", data)
    if checksum(data) == 0:
        c.send(b"No Error")
    else:
        c.send(b"Error Detected")
    c.close()