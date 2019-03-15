from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5


def encryption_place(plain_txt):
    public_key=private_key.publickey()
    pubDash = PKCS1_v1_5.new(public_key)
    return pubDash.encrypt(plain_txt)

def key_generation():
    random_generator = Random.new().read
    return RSA.generate(1024, random_generator)

def save_Keys():
    with open("privateKey.pem", "wb") as prfile:
        prfile.write(private_key.exportKey('PEM'))

if __name__ == '__main__':
    private_key = key_generation()
    key_generation()
    save_Keys()
    print(encryption_place(b'8872383735'))