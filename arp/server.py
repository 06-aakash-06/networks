import socket

table = {
    "192.168.1.1": "AA:BB:CC:DD:EE:01",
    "192.168.1.2": "AA:BB:CC:DD:EE:02",
    "192.168.1.3": "AA:BB:CC:DD:EE:03"
}

s = socket.socket()
s.bind(("localhost", 5000))
s.listen()

while True:
    c, addr = s.accept()
    mode, value = c.recv(1024).decode().split("|")

    result = "Not Found"

    if mode == "ARP":
        result = table.get(value, "Not Found")

    elif mode == "RARP":
        for ip, mac in table.items():
            if mac == value:
                result = ip
                break

    c.send(result.encode())
    c.close()