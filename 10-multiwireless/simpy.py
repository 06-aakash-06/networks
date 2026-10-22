import simpy
import random
#multiwireless
nodes = {
    "W1": "Laptop", "W2": "Smartphone", "W3": "Camera",
    "B1": "Smartphone", "B2": "Watch", "B3": "Sensor",
    "Z1": "Temperature", "Z2": "Light", "Z3": "Environment"
}
def send(env, src, dst, n, size, interval, loss, delay, distance, rng, rate):
    received = 0
    delays = []
    for i in range(1, n + 1):
        yield env.timeout(interval)
        start = env.now
        if distance > rng:
            print(src, "->", dst, "Packet", i, "Out of range")
            continue
        d = random.uniform(delay[0], delay[1])
        yield env.timeout(d + size * 8 / rate)
        if random.random() < loss:
            print(src, "->", dst, "Packet", i, "Lost")
        else:
            received += 1
            delays.append(env.now - start)
            print(src, "->", dst, "Packet", i, "Received")
    print("\n", src, "->", dst)
    print("Generated:", n)
    print("Received:", received)
    print("Lost:", n - received)
    print("Delivery Ratio:", received / n * 100, "%")
    if received > 0:
        print("Average Delay:", sum(delays) / received)
        print("Minimum Delay:", min(delays))
        print("Maximum Delay:", max(delays))
    print("Throughput:", received * size * 8 / env.now, "bps")
def run():
    random.seed(42)
    env = simpy.Environment()
    print("Nodes:", nodes)
    env.process(send(env, "W1", "W2", 20, 1024, 0.2,
                     0.02, (0.005, 0.02), 20, 100, 50000000))
    env.process(send(env, "B1", "B2", 15, 256, 0.5,
                     0.05, (0.01, 0.05), 5, 10, 2000000))
    env.process(send(env, "Z1", "Z2", 20, 100, 1,
                     0.03, (0.02, 0.1), 20, 50, 250000))
    env.process(send(env, "W3", "W1", 20, 1024, 0.2,
                     0.02, (0.005, 0.02), 20, 100, 50000000))
    env.process(send(env, "B3", "B1", 15, 256, 0.5,
                     0.05, (0.01, 0.05), 5, 10, 2000000))
    env.process(send(env, "Z3", "Z1", 20, 100, 1,
                     0.03, (0.02, 0.1), 20, 50, 250000))

    env.process(send(env, "B1", "B3", 10, 256, 0.5,
                     0.05, (0.01, 0.05), 25, 10, 2000000))

    env.run()

run()