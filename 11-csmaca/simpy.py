import simpy
import random

def node(env, name, channel, cwmin, cwmax, packets):
    success = 0
    collisions = 0

    for i in range(packets):
        cw = cwmin

        for attempt in range(5):
            backoff = random.randint(0, cw - 1)

            while backoff > 0:
                yield env.timeout(1)
                if not channel["busy"]:
                    backoff -= 1

            while channel["busy"]:
                yield env.timeout(1)

            slot = env.now
            channel["attempts"][slot] = channel["attempts"].get(slot, 0) + 1

            yield env.timeout(0)

            if channel["attempts"][slot] > 1:
                collisions += 1
                cw = min(cw * 2, cwmax)
                print(name, "Collision")
                yield env.timeout(1)
            else:
                channel["busy"] = True
                yield env.timeout(2)
                channel["busy"] = False
                success += 1
                print(name, "Packet", i + 1, "Sent")
                break

    print(name, "Success:", success, "Collisions:", collisions)

def run(n, cwmin, cwmax, packets):
    random.seed(42)
    env = simpy.Environment()
    channel = {"busy": False, "attempts": {}}

    for i in range(n):
        env.process(node(env, "N" + str(i + 1),
                         channel, cwmin, cwmax, packets))

    env.run()

run(2, 4, 16, 20)
run(5, 4, 16, 20)
run(5, 2, 8, 20)
run(5, 8, 16, 20)
run(10, 4, 16, 20)