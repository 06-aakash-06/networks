import socket
import random
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 5000))

loss = float(input("Loss probability (0-1): "))
low = float(input("Minimum delay: "))
high = float(input("Maximum delay: "))

while True:
    data, addr = s.recvfrom(1024)

    if random.random() < loss:
        print("Lost:", data.decode())
        continue

    time.sleep(random.uniform(low, high))
    s.sendto(data, addr)
    print("Received:", data.decode())