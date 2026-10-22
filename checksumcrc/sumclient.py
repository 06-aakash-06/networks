import socket

def checksum(data):
    total = sum(data)
    while total > 255:
        total = total % 256 + total // 256
    return 255 - total

s = socket.socket()
s.connect(("localhost", 5000))

data = list(map(int, input("Enter data: ").split()))
cs = checksum(data)

print("Checksum:", cs)

data.append(cs)
s.send(" ".join(map(str, data)).encode())

print("Server:", s.recv(1024).decode())

s.close()