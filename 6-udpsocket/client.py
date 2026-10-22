import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(0.5)

n = int(input("Packets: "))
size = int(input("Packet size: "))
interval = float(input("Interval: "))
received = 0
delays = []
start = time.perf_counter()

for i in range(n):
    packet = str(i).encode()
    packet = packet.ljust(size, b"0")

    sent = time.perf_counter()
    s.sendto(packet, ("localhost", 5000))

    try:
        data, addr = s.recvfrom(1024)
        received += 1
        delays.append(time.perf_counter() - sent)
        print("Received:", i)
    except socket.timeout:
        print("Lost:", i)

    time.sleep(interval)

total = time.perf_counter() - start

print("Generated:", n)
print("Received:", received)
print("Lost:", n - received)
print("PDR:", received / n * 100, "%")
print("Throughput:", received * size * 8 / total, "bps")

if received:
    print("Average RTT:", sum(delays) / received)

s.close()