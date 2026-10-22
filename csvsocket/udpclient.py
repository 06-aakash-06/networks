import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    roll = input("Enter roll number: ")
    if roll == "exit":
        break

    s.sendto(roll.encode(), ("localhost", 5001))
    data, addr = s.recvfrom(1024)
    print(data.decode())

s.close()