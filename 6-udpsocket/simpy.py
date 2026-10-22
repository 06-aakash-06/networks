import simpy
import random
#udpsimpy
def send(env, ch, packet, loss, delay):
    if random.random() < loss:
        print("Lost:", packet)
        return
    yield env.timeout(random.uniform(delay[0], delay[1]))
    yield ch.put((packet, env.now))

def client(env, ch, n, size, interval, loss, delay):
    for i in range(n):
        yield env.timeout(interval)
        print("Generated:", i)
        env.process(send(env, ch, i, loss, delay))

def server(env, ch, received):
    while True:
        packet, time = yield ch.get()
        received.append((packet, time))
        print("Received:", packet, "at", time)

def run(n, size, interval, loss, delay):
    random.seed(42)
    env = simpy.Environment()
    ch = simpy.Store(env)
    received = []

    env.process(client(env, ch, n, size, interval, loss, delay))
    env.process(server(env, ch, received))
    env.run()

    print("Generated:", n)
    print("Received:", len(received))
    print("Lost:", n - len(received))
    print("PDR:", len(received) / n * 100, "%")
    print("Throughput:", len(received) * size * 8 / env.now, "bps")
    print()

run(10, 100, 0.2, 0, (0, 0))
run(20, 100, 0.2, 0.1, (0.01, 0.05))
run(30, 200, 0.1, 0.2, (0.02, 0.1))
run(50, 200, 0.067, 0.3, (0.05, 0.15))