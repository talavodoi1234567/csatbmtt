from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

iv = b'initialvector123'

def data_encrypt(key, data):
    # data = data.encode()
    data = pad(data.encode(), AES.block_size)
    # key = key.encode()
    key = pad(key.encode(), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

def data_decrypt(key, data):
    # key = key.encode()
    key = pad(key.encode(), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(data)
    try:
        unpadded_data = unpad(decrypted_data, AES.block_size)
    except ValueError:
        return decrypted_data.decode('ISO-8859-1')
    else:
        return unpadded_data.decode('ISO-8859-1')

if __name__ == '__main__':
    key = 'this is the key'

    data = 'this is the data'
    # cipher = AES.new(key, AES.MODE_CBC, iv)  # táº¡o Äá»i tÆ°á»£ng cipher

    encrypted_data = data_encrypt(key, data)


    # key = 'this is not the key'
    decrypted_data = data_decrypt(key, encrypted_data)

    print("Data: {}".format(data))
    print("Encrypted data: {}".format(encrypted_data.decode('ISO-8859-1')))
    print(f"Decrypted data: {decrypted_data}")
