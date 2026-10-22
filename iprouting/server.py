import socket

ips = {
    "PC1": "192.168.1.10",
    "PC2": "192.168.1.20",
    "PC3": "192.168.1.30",
    "PC4": "192.168.2.10",
    "PC5": "192.168.3.20",
    "PC6": "192.168.3.30"
}

routes = {
    "R1": {"1": "PC", "2": "R2", "3": "R2"},
    "R2": {"1": "R1", "2": "PC", "3": "R3"},
    "R3": {"1": "R2", "2": "R2", "3": "PC"}
}

def route(src, dst):
    if src not in ips or dst not in ips:
        return "Destination not found"

    srcnet = ips[src].split(".")[2]
    dstnet = ips[dst].split(".")[2]
    path = [src]

    if srcnet != dstnet:
        router = "R" + srcnet

        while True:
            path.append(router)
            next_hop = routes[router].get(dstnet)

            if next_hop is None:
                return "No Route"

            if next_hop == "PC":
                break

            router = next_hop

    path.append(dst)
    return " -> ".join(path)

s = socket.socket()
s.bind(("localhost", 5000))
s.listen()

while True:
    c, addr = s.accept()
    src, dst = c.recv(1024).decode().split(",")
    c.send(route(src, dst).encode())
    c.close()