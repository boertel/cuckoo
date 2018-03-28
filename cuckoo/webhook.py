import hashlib
import hmac
import base64


def make_digest(message, key):
    key = bytes(key, 'UTF-8')
    message = bytes(message, 'UTF-8')
    digester = hmac.new(key, message, hashlib.sha1)
    signature = digester.digest()
    signature_b64 = base64.urlsafe_b64encode(signature)
    return str(signature_b64, 'UTF-8')
