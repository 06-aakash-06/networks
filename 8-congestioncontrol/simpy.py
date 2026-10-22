import simpy
import random

def reno(env, n, loss, rtt):
    cwnd = 1
    ssthresh = 8
    sent = 0
    while sent < n:
        yield env.timeout(rtt)
        if random.random() < loss:
            ssthresh = max(1, cwnd / 2)
            cwnd = 1
            print("Reno Loss:", cwnd)
        else:
            sent += min(int(cwnd), n - sent)
            if cwnd < ssthresh:
                cwnd *= 2
            else:
                cwnd += 1
            print("Reno ACK:", cwnd)

def cubic(env, n, loss, rtt):
    cwnd = 1
    sent = 0
    t = 0
    maximum = 1
    while sent < n:
        yield env.timeout(rtt)
        if random.random() < loss:
            maximum = cwnd
            cwnd = max(1, cwnd * 0.7)
            t = 0
            print("CUBIC Loss:", cwnd)
        else:
            sent += min(int(cwnd), n - sent)
            t += rtt
            k = ((maximum * 0.3) / 0.4) ** (1 / 3)
            cwnd = max(1, 0.4 * (t - k) ** 3 + maximum)
            print("CUBIC ACK:", round(cwnd, 2))

def bbr(env, n, loss, rtt, bandwidth):
    cwnd = 1
    sent = 0
    while sent < n:
        yield env.timeout(rtt)
        if random.random() < loss:
            print("BBR Packet Lost")
        else:
            sent += min(int(cwnd), n - sent)
        cwnd = max(1, bandwidth * 1000000 * rtt / 8000)
        print("BBR cwnd:", round(cwnd, 2))

def run(name):
    random.seed(42)
    env = simpy.Environment()

    if name == "Reno":
        env.process(reno(env, 100, 0.02, 0.02))
    elif name == "CUBIC":
        env.process(cubic(env, 100, 0.02, 0.02))
    else:
        env.process(bbr(env, 100, 0.02, 0.02, 10))

    env.run()
    print("Time:", round(env.now, 3), "seconds")
    print("Throughput:", round(100 * 8000 / env.now / 1000000, 3), "Mbps")

run("Reno")
run("CUBIC")
run("BBR")