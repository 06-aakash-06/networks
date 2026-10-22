import socket

def checksum(data):
    total = sum(data)
    while total > 255:
        total = total % 256 + total // 256
    return 255 - total

s = socket.socket()
s.bind(("localhost", 5000))
s.listen(1)

c, addr = s.accept()

data = list(map(int, c.recv(1024).decode().split()))

if checksum(data) == 0:
    print("No Error")
    c.send(b"No Error")
else:
    print("Error Detected")
    c.send(b"Error Detected")

c.close()
s.close()