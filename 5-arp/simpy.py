import simpy

table = {
    "192.168.1.1": "AA:BB:CC:DD:EE:01",
    "192.168.1.2": "AA:BB:CC:DD:EE:02",
    "192.168.1.3": "AA:BB:CC:DD:EE:03"
}

def resolve(env, mode, value):
    print(mode, "Request:", value)

    yield env.timeout(1)

    result = "Not Found"

    if mode == "ARP":
        result = table.get(value, "Not Found")

    elif mode == "RARP":
        for ip, mac in table.items():
            if mac == value:
                result = ip
                break

    print(mode, "Reply:", result)

env = simpy.Environment()

env.process(resolve(env, "ARP", "192.168.1.2"))
env.process(resolve(env, "RARP", "AA:BB:CC:DD:EE:03"))

env.run()