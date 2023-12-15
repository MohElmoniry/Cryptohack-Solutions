from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import *
import hashlib

a = 497
b = 1768
p = 9739
G = (1804, 5368)


def add_point(p1, p2):
    if p1 == (0, 0):
        return p2
    if p2 == (0, 0):
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 == -y2:
        return (0, 0)

    lamda = 0
    if p1 == p2:
        lamda = ((3 * pow(x1, 2, p) + a) * inverse(2 * y1, p))
    else:
        lamda = ((y2 - y1) * inverse(x2 - x1, p))

    x3 = (pow(lamda, 2) - x1 - x2) % p
    y3 = (lamda * (x1 - x3) - y1) % p
    return (x3, y3)


def Scalar_Mul(P, n):
    Q = P
    R = (0, 0)
    while n > 0:
        # If n ≡ 1 mod 2, set R = R + Q.
        if n % 2 == 1:
            R = add_point(R, Q)
        # Set Q = 2 Q and n = ⌊n/2⌋.
        Q = add_point(Q, Q)
        n = n // 2
    return R


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')


# E: Y^2 = X^3 + 497 X + 1768, p: 9739, G: (1804,5368)
q_x = 4726
nB = 6534
y_2 = (pow(q_x, 3) + 497 * q_x + 1768) % p
q_y = pow(y_2, (p + 1) // 4, p)
Q = (q_x, q_y)

shared_secret = Scalar_Mul(Q, nB)[0]
iv = 'cd9da9f1c60925922377ea952afc212c'
ciphertext = 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'

print(decrypt_flag(shared_secret, iv, ciphertext))