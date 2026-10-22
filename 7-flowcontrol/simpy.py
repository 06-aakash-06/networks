import simpy
#flowcontrol
def server(env, buffer, size, rate):
    while True:
        while buffer.level < size:
            yield env.timeout(0.01)
        yield env.timeout(size / rate)
        yield buffer.get(size)
        print("Processed at:", round(env.now, 2))
def client(env, buffer, n, size, rate, delay):
    for i in range(n):
        yield env.timeout(size / rate + delay)
        yield buffer.put(size)
        print("Sent:", i + 1, "at", round(env.now, 2))
def run(n, size, capacity, recv_rate, send_rate, delay):
    env = simpy.Environment()
    buffer = simpy.Container(env, capacity=capacity)
    env.process(server(env, buffer, size, recv_rate))
    env.process(client(env, buffer, n, size, send_rate, delay))
    env.run(until=20)
run(20, 1, 4, 4, 8, 0.1)

