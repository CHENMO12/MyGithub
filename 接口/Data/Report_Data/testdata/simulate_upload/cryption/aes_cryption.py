"""
    AES crypto, need assign Key
        UTF-8 str
            128bit-ECB-PKCS5Padding
"""
from binascii import b2a_base64, a2b_base64
from Crypto.Cipher import AES

'PKCS5Padding'
BS = AES.block_size
'bytes type'
pad = lambda s: s + (BS - len(s) % BS) * bytes((BS - len(s) % BS,))
unpad = lambda s: s[0:-int(s[-1])]


# 'str type'
# str_pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
# str_unpad = lambda s: s[0:-ord(s[-1])]


class ReAES(object):
    key_bits = 2 ** 7
    key_length = key_bits // (2 ** 3)
    encoding_name = 'utf-8'

    def __init__(self, _key):
        self.key = self.check_key(_key)
        self.mode = AES.MODE_ECB
        self.aes = AES.new(self.key.encode(self.encoding_name), self.mode)

    def check_key(self, a_key):
        if isinstance(a_key, str):
            if len(a_key) == self.key_length:
                return a_key
            raise RuntimeError("err key length: expected : %d, actual : %d" % (self.key_length, len(a_key)))
        raise RuntimeError("err key type: expected : %s, actual : %s" % (str, type(a_key)))

    def encrypt(self, _plain_text):
        _plain_text = pad(_plain_text)
        _encode_text = self.aes.encrypt(_plain_text)
        return _encode_text

    def decrypt(self, _encode_text):
        _plain_text = self.aes.decrypt(_encode_text)
        _plain_text = unpad(_plain_text)
        return _plain_text

    def str_encrypt(self, _str_plain_text):
        bytes_plain_text = bytes(_str_plain_text, encoding=self.encoding_name)
        bytes_encode_text = self.encrypt(bytes_plain_text)
        return str(b2a_base64(bytes_encode_text), encoding=self.encoding_name)

    def str_decrypt(self, _str_encode_text):
        bytes_encode_text = a2b_base64(_str_encode_text)
        bytes_plain_text = self.decrypt(bytes_encode_text)
        return str(bytes_plain_text, encoding=self.encoding_name)


class ReRSA(object):
    def __init__(self, public_key, private_key=''):
        self.public_key = public_key
        self.private_key = private_key

    def publicKey_encrypt(self, _plain_text):
        pass

    def publicKey_decrypt(self, _encode_text):
        pass


if __name__ == "__main__":
    'aes for example'
    key = "B5MrV4zU1Wro36Cy"
    aes = ReAES(key)

    # plain_text = b'123'
    # str_plain_text = 'this is the block one'
    #
    # encode_text = aes.encrypt(plain_text)
    # print(encode_text)
    # print(aes.decrypt(encode_text))
    #
    # str_encode_text = aes.str_encrypt(str_plain_text)
    # print(str_encode_text)
    # print(aes.str_decrypt(str_encode_text))

    encode_text = b'\xd4\xf6g\x89\xee,.=ez\xae\xc6*\x0e\x92i'

    print(aes.decrypt(encode_text))