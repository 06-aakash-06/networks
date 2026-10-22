import simpy

def checksum(data):
    total = sum(data)
    while total > 255:
        total = total % 256 + total // 256
    return 255 - total

def sender(env, data):
    cs = checksum(data)
    print("Sender:", data, "Checksum:", cs)

    yield env.timeout(1)

    receiver(data + [cs])

def receiver(data):
    print("Receiver:", data)

    if checksum(data) == 0:
        print("No Error")
    else:
        print("Error Detected")

env = simpy.Environment()
env.process(sender(env, [100, 150, 200]))
env.run()