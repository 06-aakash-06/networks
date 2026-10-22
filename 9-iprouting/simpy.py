import simpy

#iprouting
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
def network(ip):
    return ip.split(".")[2]
def send(env, src, dst):
    start = env.now
    srcnet = network(ips[src])
    dstnet = network(ips.get(dst, dst))
    path = [src]
    hops = 0
    if srcnet == dstnet:
        yield env.timeout(0.01)
    else:
        router = "R" + srcnet

        while True:
            yield env.timeout(0.01)
            path.append(router)
            yield env.timeout(0.005)
            hops += 1
            if dstnet not in routes[router]:
                print(src, "->", dst, "DROPPED")
                return
            next_hop = routes[router][dstnet]
            if next_hop == "PC":
                yield env.timeout(0.01)
                break
            router = next_hop
    path.append(dst)
    print("Path:", " -> ".join(path))
    print("Hops:", hops)
    print("Delay:", round((env.now - start) * 1000), "ms")
    
def run(src, dst):
    env = simpy.Environment()
    env.process(send(env, src, dst))
    env.run()
run("PC1", "PC2")
run("PC1", "PC4")
run("PC2", "PC5")
run("PC6", "PC3")
run("PC1", "192.168.4.10")


