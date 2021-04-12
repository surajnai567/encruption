from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC
import base64


def get_rand_key(n=16):
    return get_random_bytes(n)


def read_file(filename):
    with open(filename, "rb")as f:
        return f.read()


def write_to_file(filename, data):
    with open(filename, 'wb+') as f:
        f.write(data)


write_to_file('pt1.txt', b'This is the test message 1')
key = get_rand_key(8)
data1 = read_file('pt1.txt')
cipher = HMAC.new(key)
ciphered_data1 = cipher.update(data1).digest()
base_encoded_1 = base64.b64encode(ciphered_data1)

write_to_file('pt1.txt', b'This is the test message 2')
data2 = read_file('pt1.txt')
cipher2 = HMAC.new(key)
ciphered_data2 = cipher2.update(data2).digest()
base_encoded_2 = base64.b64encode(ciphered_data2)

# save to a file name c1 c2
write_to_file('tag1.txt', base_encoded_1)
write_to_file('tag2.txt', base_encoded_2)

# read and confirm cipher is different
c1 = read_file('tag1.txt')
c2 = read_file('tag2.txt')
print("hash 1: ", c1)
print("hash 2: ", c2)