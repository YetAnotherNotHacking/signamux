from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import os

# func for deriving a key from password and salt.
# it is very very importabt that this salt is stored somewhere in the file!
def _derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)

    return kdf.derive(password)

# raw byte password encryption
def encrypt_bytes(password:str, data:bytes) -> bytes:
    password_b = password.encode() # conv pw to bytes
    salt = os.urandom(16) # gen salt
    key = _derive_key(password_b, salt) # derive key from pw and salt
    aes = AESGCM(key) # set up aes cipher
    nonce = os.urandom(12) # gen a nonce value
    ct = aes.encrypt(nonce, data, None)
    
    return salt + nonce + ct

def decrypt_bytes(password: str, blob:bytes) -> bytes:
    salt = blob[:16]
    nonce = blob[16:28]
    ct = blob[28:]
    key = _derive_key(password.encode(), salt)
    
    return AESGCM(key).decrypt(nonce, ct, None)