from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import base64


def get_rand_key(n=16):
    return get_random_bytes(n)


def read_file(filename):
    with open(filename, "rb")as f:
        return f.read()


def write_to_file(filename, data):
    with open(filename, 'wb+') as f:
        f.write(data)


data1 = read_file('pt1.txt')
data2 = read_file('pt2.txt')
cipher = AES.new(get_rand_key(), AES.MODE_ECB)
ciphered_data1 = cipher.encrypt(pad(data1, AES.block_size))
base_encoded_1 = base64.b64encode(ciphered_data1)

ciphered_data2 = cipher.encrypt(pad(data2, AES.block_size))
base_encoded_2 = base64.b64encode(ciphered_data2)

# save to a file name c1 c2
write_to_file('ct1.txt', base_encoded_1)
write_to_file('ct2.txt', base_encoded_2)

# read and confirm cipher is same
c1 = read_file('ct1.txt')
c2 = read_file('ct2.txt')
print("cipher 1: ", c1)
print("cipher 2: ", c2)