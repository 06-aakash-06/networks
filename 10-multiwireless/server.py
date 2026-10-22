import socket
import random
import time

tech = {
    "WiFi": (100, 0.02, 0.01, 50000000),
    "Bluetooth": (10, 0.05, 0.03, 2000000),
    "Zigbee": (50, 0.03, 0.06, 250000)
}

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 5000))

while True:
    data, addr = s.recvfrom(4096)

    name, distance, packet = data.decode().split("|", 2)
    rng, loss, delay, rate = tech[name]

    if float(distance) > rng:
        print(name, "Out of range")
        continue

    if random.random() < loss:
        print(name, "Packet lost")
        continue

    time.sleep(delay + len(packet.encode()) * 8 / rate)

    s.sendto(b"Received", addr)
    print(name, "Packet received")