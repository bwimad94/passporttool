import base64
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher (object):
    def __init__(self, key):
        self.key = pad (key)

    def encryptAES(self, plainMsg):
        try:
            plainMsg = pad (plainMsg)
            iv = Random.new ().read (AES.block_size)  # adds randomsness to the start of the encryption
            cipher = AES.new (self.key, AES.MODE_CBC, iv)
            return base64.b64encode (iv + cipher.encrypt (plainMsg))
        except Exception:
            print Exception


    def decryptAES(self, cipherMsg):
        try:
            cipherMsg = base64.b64decode (cipherMsg)
            iv = cipherMsg[:16]  # get first sixteen elements as the iv
            cipher = AES.new (self.key, AES.MODE_CBC, iv)
            return unpad (cipher.decrypt (cipherMsg[16:]))
        except Exception:
            print Exception

basicString = 16
pad = lambda insString: insString + (basicString - len (insString) % basicString) * chr (basicString - len (insString) % basicString)#adds the bytes required
unpad = lambda insString: insString[:-ord (insString[len (insString) - 1:])]#removes the added bytes