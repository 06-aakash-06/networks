import simpy
import random

def node(env, name, channel, cwmin, cwmax, packets):
    success = collisions = 0
    for i in range(packets):
        cw = cwmin
        for attempt in range(5):
            backoff = random.randrange(cw)
            while backoff > 0 or channel["busy"]:
                yield env.timeout(1)
                if not channel["busy"] and backoff > 0:
                    backoff -= 1
            slot = env.now
            channel["attempts"][slot] = channel["attempts"].get(slot, 0) + 1
            yield env.timeout(0.001)
            if channel["attempts"][slot] > 1:
                collisions += 1
                cw = min(cw * 2, cwmax)
                print(name, "Collision")
            else:
                channel["busy"] = True
                yield env.timeout(2)
                channel["busy"] = False
                success += 1
                print(name, "Sent:", i + 1)
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


