import simpy
import random

def simulate(env, name, n, loss, rtt, bandwidth=10):
    cwnd, sent = 1, 0
    threshold, maximum, t = 8, 1, 0
    while sent < n:
        yield env.timeout(rtt)
        if random.random() < loss:
            if name == "Reno":
                threshold = max(1, cwnd / 2)
                cwnd = 1
            elif name == "CUBIC":
                maximum = cwnd
                cwnd = max(1, cwnd * 0.7)
                t = 0
            else:
                print("BBR Packet Lost")
            print(name, "Loss:", round(cwnd, 2))
        else:
            sent += min(int(cwnd), n - sent)
            if name == "Reno":
                if cwnd < threshold:
                    cwnd *= 2
                else:
                    cwnd += 1
            elif name == "CUBIC":
                t += rtt
                k = (maximum * 0.3 / 0.4) ** (1/3)
                cwnd = max(1, 0.4 * (t-k)**3 + maximum)
            print(name, "ACK:", round(cwnd, 2))
        if name == "BBR":
            cwnd = max(1, bandwidth * 1000000 * rtt / 8000)
            print("BBR cwnd:", round(cwnd, 2))


def run(name):
    random.seed(42)
    env = simpy.Environment()
    env.process(simulate(env, name, 100, 0.02, 0.02))
    env.run()

    print("Time:", round(env.now, 3), "seconds")
    print("Throughput:", round(100 * 8000 / env.now / 1000000, 3), "Mbps")
    print()

run("Reno")
run("CUBIC")
run("BBR")

