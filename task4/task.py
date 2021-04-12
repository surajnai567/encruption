from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
import os

BUFFER_SIZE = 1024 * 1024  # The size in bytes that we read, encrypt and write to at once
password = "password"  # Get this from somewhere else like input()

input_filename = 'pt1.txt'  # Any file extension will work
output_filename = 'ct3.txt'  # You can name this anything, I'm just putting .encrypted on the end

# Open files
file_in = open(input_filename, 'rb')  # rb = read bytes. Required to read non-text files
file_out = open(output_filename, 'wb')  # wb = write bytes. Required to write the encrypted data

salt = get_random_bytes(32)  # Generate salt
key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)  # Generate a key using the password and salt
file_out.write(salt)  # Write the salt to the top of the output file

cipher = AES.new(key, AES.MODE_GCM)  # Create a cipher object to encrypt data
file_out.write(cipher.nonce)  # Write out the nonce to the output file under the salt

# Read, encrypt and write the data
data = file_in.read(BUFFER_SIZE)  # Read in some of the file
while len(data) != 0:  # Check if we need to encrypt anymore data
    encrypted_data = cipher.encrypt(data)  # Encrypt the data we read
    file_out.write(encrypted_data)  # Write the encrypted data to the output file
    data = file_in.read(BUFFER_SIZE)  # Read some more of the file to see if there is any more left

# Get and write the tag for decryption verification
tag = cipher.digest()  # Signal to the cipher that we are done and get the tag
file_out.write(tag)

# Close both files
file_in.close()
file_out.close()


# read and confirm cipher is different

input_filename = 'ct3.txt'  # The encrypted file
output_filename = 'decrypted.txt'  # The decrypted file

# Open files
file_in = open(input_filename, 'rb')
file_out = open(output_filename, 'wb')

# Read salt and generate key
salt = file_in.read(32)  # The salt we generated was 32 bits long
key = scrypt(password, salt, key_len=32, N=2**17, r=8, p=1)  # Generate a key using the password and salt again

# Read nonce and create cipher
nonce = file_in.read(16)  # The nonce is 16 bytes long
cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

file_in_size = os.path.getsize(input_filename)
encrypted_data_size = file_in_size - 32 - 16 - 16  # Total - salt - nonce - tag = encrypted data

# Read, decrypt and write the data
for _ in range(int(encrypted_data_size / BUFFER_SIZE)):  # Identify how many loops of full buffer reads we need to do
    data = file_in.read(BUFFER_SIZE)  # Read in some data from the encrypted file
    decrypted_data = cipher.decrypt(data)  # Decrypt the data
    file_out.write(decrypted_data)  # Write the decrypted data to the output file
data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))  # Read whatever we have calculated to be left of encrypted data
decrypted_data = cipher.decrypt(data)  # Decrypt the data
print("decrupted data :", decrypted_data)  # Write the decrypted data to the output file

# change a character of file
change_cipher = open('ct3.txt', 'wb+')
change_cipher.seek(0,0)
change_cipher.write(b'm')
change_cipher.close()

for _ in range(int(encrypted_data_size / BUFFER_SIZE)):  # Identify how many loops of full buffer reads we need to do
    data = file_in.read(BUFFER_SIZE)  # Read in some data from the encrypted file
    decrypted_data = cipher.decrypt(data)  # Decrypt the data
    file_out.write(decrypted_data)  # Write the decrypted data to the output file
data = file_in.read(int(encrypted_data_size % BUFFER_SIZE))  # Read whatever we have calculated to be left of encrypted data
decrypted_data = cipher.decrypt(data)  # Decrypt the data
print("decrupted data after changing:", decrypted_data)

tag = file_in.read(16)
try:
    cipher.verify(tag)
except ValueError as e:
    # If we get a ValueError, there was an error when decrypting so delete the file we created
    file_in.close()
    file_out.close()
    os.remove(output_filename)
    raise e

# If everything was ok, close the files
file_in.close()
file_out.close()

