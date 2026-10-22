import simpy

def divide(bits, key):
    bits = list(bits)
    for i in range(len(bits) - len(key) + 1):
        if bits[i] == '1':
            for j in range(len(key)):
                bits[i+j] = str(int(bits[i+j]) ^ int(key[j]))
    return ''.join(bits[-(len(key)-1):])

def sender(env, data, key):
    crc = divide(data + '0' * (len(key) - 1), key)
    codeword = data + crc

    print("CRC:", crc)
    print("Transmitted:", codeword)

    yield env.timeout(1)

    receiver(codeword, key)

def receiver(codeword, key):
    remainder = divide(codeword, key)

    print("Remainder:", remainder)

    if int(remainder) == 0:
        print("No Error")
    else:
        print("Error Detected")

env = simpy.Environment()
env.process(sender(env, "1101011011", "10011"))
env.run()