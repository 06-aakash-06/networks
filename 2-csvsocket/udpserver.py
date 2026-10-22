import socket
import threading
import csv

def handle(roll, addr):
    result = "Not Found"

    with open("students.csv", "r") as f:
        for row in csv.reader(f):
            if row[0] == roll:
                result = str(row)
                break

    s.sendto(result.encode(), addr)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", 5001))

while True:
    data, addr = s.recvfrom(1024)
    threading.Thread(
        target=handle,
        args=(data.decode(), addr)
    ).start()