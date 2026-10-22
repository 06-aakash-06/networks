import socket

def divide(bits, key):
    bits = list(bits)
    for i in range(len(bits) - len(key) + 1):
        if bits[i] == '1':
            for j in range(len(key)):
                bits[i+j] = str(int(bits[i+j]) ^ int(key[j]))
    return ''.join(bits[-(len(key)-1):])

s = socket.socket()
s.connect(('localhost', 5000))

data = input("Enter data: ")
key = input("Enter key: ")

bits = data + '0' * (len(key) - 1)
crc = divide(bits, key)

print("CRC:", crc)

codeword = data + crc
print("Transmitted:", codeword)

s.send((codeword + ',' + key).encode())
s.close()