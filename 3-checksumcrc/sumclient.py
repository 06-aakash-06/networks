import socket

def checksum(data):
    total = sum(data)
    while total > 255:
        total = total % 256 + total // 256
    return 255 - total
s = socket.socket()
s.connect(("localhost", 5000))
data = []
for x in input("Enter data: ").split():
    data.append(int(x))
cs = checksum(data)
print("Checksum:", cs)
data.append(cs)
if input("Introduce error? (y/n): ") == "y":
    data[0] += 1
msg = ""
for x in data:
    msg += str(x) + " "
s.send(msg.encode())
print("Server:", s.recv(1024).decode())
s.close()