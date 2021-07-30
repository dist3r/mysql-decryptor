from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from Crypto.Util.Padding import unpad


def microsoft_password_derive_bytes(passphrase, salt, iterations, key_length):
    if iterations < 1:
        raise ValueError('Number of iterations must be at least 1!')

    salted_passphrase_bytes = passphrase.encode('utf-8') + salt.encode('utf-8')
    last_derived_key = SHA1.new(salted_passphrase_bytes).digest()

    for i in range(iterations - 2):
        last_derived_key = SHA1.new(last_derived_key).digest()
    derived_key = SHA1.new(last_derived_key).digest()

    i = 1
    while len(derived_key) < key_length:
        derived_key += SHA1.new(str(i).encode('utf-8') + last_derived_key).digest()
        i += 1

    return derived_key[:key_length]


def decrypt(ciphertext_bytes, passphrase, initialization_vector):
    key = microsoft_password_derive_bytes(passphrase, '', 100, 32)
    initialization_vector_bytes = initialization_vector.encode('utf-8')

    cipher = AES.new(key, AES.MODE_CBC, iv=initialization_vector_bytes)
    return unpad(cipher.decrypt(ciphertext_bytes), AES.block_size).decode('utf-8')
