from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import chardet

def decoding(bytes_data):
    detected_encoding = chardet.detect(bytes_data)['encoding']
    str_data = bytes_data.decode(detected_encoding)
    return str_data

def encoding(str_data):
    detected_encoding = chardet.detect(str_data.encode())['encoding']
    bytes_data = str_data.encode(detected_encoding)
    return bytes_data

if __name__ == '__main__':
# Define the key and initialization vector (IV)
    key = 'secretkey123456'
    iv = b'initialvector123'

    # Create an AES cipher object for encryption
    key = pad(encoding(key), AES.block_size)

    # The plaintext to be encrypted
    plaintext = 'This is a secret message'

    plaintext = encoding(plaintext)
    # Pad the plaintext to the AES block size
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = pad(plaintext, AES.block_size)

    # Encrypt the plaintext
    ciphertext = cipher.encrypt(plaintext)
    ciphertext2 = decoding(ciphertext)
    decrypt_cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext2 = encoding(ciphertext2)
    # Decrypt the ciphertext
    decrypted_data = decrypt_cipher.decrypt(ciphertext2)

    # Unpad the decrypted data
    unpadded_data = unpad(decrypted_data, AES.block_size)

    unpadded_data = decoding(unpadded_data)

    # Print the decrypted message
    print(plaintext)
    print(ciphertext)
    print(unpadded_data)
