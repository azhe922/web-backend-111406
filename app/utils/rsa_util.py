from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii


def decrypt_token(data: bytes):

    # 要解密的資料（必須為 bytes）
    ciphertext = binascii.unhexlify(data)
    # 獲取私鑰檔案路徑
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # data_file = os.path.join(basedir, r'..\..\keys\WebBackend_PrivateKey.pem')
    data_file = '/etc/secrets/WebBackend_PrivateKey.pem'
    # 讀取 RSA 私鑰
    key = RSA.import_key(open(data_file).read())

    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    return plaintext

def encrypt(data: bytes):
    # 獲取公鑰檔案路徑
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # data_file = os.path.join(basedir, r'..\..\keys\FCM_PublicKey.pem')
    data_file = '/etc/secrets/FCM_PublicKey.pem'

    # 讀取 RSA 公鑰
    key = RSA.import_key(open(data_file).read())

    encryptor = PKCS1_OAEP.new(key)
    encrypted = encryptor.encrypt(data)
    return binascii.hexlify(encrypted)