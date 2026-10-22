import socket

def divide(bits, key):
    bits = list(bits)
    for i in range(len(bits) - len(key) + 1):
        if bits[i] == '1':
            for j in range(len(key)):
                bits[i+j] = str(int(bits[i+j]) ^ int(key[j]))
    return ''.join(bits[-(len(key)-1):])
s = socket.socket()
s.bind(('localhost', 5000))
s.listen(1)
c, addr = s.accept()
msg = c.recv(1024).decode()
bits, key = msg.split(',')
if int(divide(bits, key)) == 0:
    print("No Error")
else:
    print("Error Detected")

c.close()
s.close()