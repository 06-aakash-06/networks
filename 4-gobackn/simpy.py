import simpy

def sender(env, n, w, lost, acklost):
    base = 0
    expected = 0
    dropped = set()
    skipped = set()

    while base < n:
        end = min(base + w, n)
        ack = base

        for frame in range(base, end):
            yield env.timeout(1)

            if frame in lost and frame not in dropped:
                dropped.add(frame)
                print("Lost:", frame)

            elif frame == expected:
                expected += 1
                print("Received:", frame)

            else:
                print("Discarded:", frame)

            if expected in acklost and expected not in skipped:
                skipped.add(expected)
                print("Lost ACK:", expected)
            else:
                ack = expected
                print("ACK:", ack)

        if ack == base:
            print("Timeout at:", env.now)
            yield env.timeout(2)

        base = ack

env = simpy.Environment()
env.process(sender(env, 10, 4, {2, 6}, {3, 7}))
env.run()