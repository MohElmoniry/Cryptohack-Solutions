from Crypto.Util.number import *
import hashlib

# E: Y^2 = X^3 + 497 X + 1768, p: 9739, G: (1804,5368)

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


Q_A = (815, 3190)
n_B = 1829

# s = n_B * Q_A
s = Scalar_Mul(Q_A, n_B)
# Generate a key by calculating the SHA1 hash of the&nbsp;x&nbsp;coordinate
s = hashlib.sha1(str(s[0]).encode()).hexdigest()

print("crypto{" + s + "}")