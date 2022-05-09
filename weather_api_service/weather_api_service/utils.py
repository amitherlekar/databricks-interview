from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode


def getBytesFromString(string: str) -> bytes:
    return string.encode('utf-8')


def getStringFromBytes(byte: bytes) -> str:
    return byte.decode('utf-8')


def getCrypt(secret_key: str) -> any:
    key = getBytesFromString(secret_key)
    cipher = AES.new(b64decode(key), AES.MODE_ECB)
    return cipher


def encrypt(secret_key: str, plain_text: str) -> str:
    cipher = getCrypt(secret_key)
    plain_text_padded = pad(getBytesFromString(plain_text), AES.block_size)
    cipher_enc = cipher.encrypt(plain_text_padded)
    encrypted_encoded = b64encode(cipher_enc)
    return encrypted_encoded


def decrypt(secret_key: str, encrypted_text: str) -> str:
    cipher = getCrypt(secret_key)
    encrypted_text_bytes = getBytesFromString(encrypted_text)
    decoded = b64decode(encrypted_text_bytes)
    decrypted = cipher.decrypt(decoded)
    decrypted_unpadded = unpad(decrypted, AES.block_size)
    return decrypted_unpadded


def getResponseHeaders() -> dict:
    return dict({
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Credentials': '*'
    })