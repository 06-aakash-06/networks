import socket

s = socket.socket()
s.connect(("localhost", 5000))

mode = input("ARP or RARP: ").upper()
value = input("Enter IP/MAC: ")

s.send((mode + "|" + value).encode())

print("Result:", s.recv(1024).decode())

s.close()