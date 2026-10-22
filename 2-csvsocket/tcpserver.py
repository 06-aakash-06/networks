import socket
import threading
import csv

def handle(c):
    while True:
        roll = c.recv(1024).decode()
        if not roll or roll == "exit":
            break

        result = "Not Found"

        with open("students.csv", "r") as f:
            for row in csv.reader(f):
                if row[0] == roll:
                    result = str(row)
                    break

        c.send(result.encode())

    c.close()

s = socket.socket()
s.bind(("localhost", 5000))
s.listen()

while True:
    c, addr = s.accept()
    threading.Thread(target=handle, args=(c,)).start()