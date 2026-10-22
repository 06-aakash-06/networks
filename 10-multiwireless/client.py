import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(1)

name = input("WiFi / Bluetooth / Zigbee: ")
distance = float(input("Distance: "))
n = int(input("Packets: "))

received = 0
start = time.perf_counter()

for i in range(n):
    packet = "Packet" + str(i + 1)
    msg = name + "|" + str(distance) + "|" + packet

    s.sendto(msg.encode(), ("localhost", 5000))

    try:
        data, addr = s.recvfrom(1024)
        print(packet, data.decode())
        received += 1
    except socket.timeout:
        print(packet, "Lost or out of range")

total = time.perf_counter() - start

print("Generated:", n)
print("Received:", received)
print("Lost:", n - received)
print("Delivery Ratio:", received / n * 100, "%")
print("Throughput:", received * 8 * 7 / total, "bps")

s.close()