from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import binascii


def decrypt_token(data: bytes):

    # 要加密的資料（必須為 bytes）
    ciphertext = binascii.unhexlify(data)    
    # 獲取公鑰檔案路徑
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_file = os.path.join(basedir, r'..\..\keys\WebBackend_PrivateKey.pem')
    # 讀取 RSA 公鑰
    key = RSA.import_key(open(data_file).read())

    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    return plaintext