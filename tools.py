import random


class T(object):
    def __init__(self, p, d):
        self.p = p
        self.d = d


def extended_euclidean_algorithm(a, b):
    """
    Returns a three-tuple (gcd, x, y) such that
    a * x + b * y == gcd, where gcd is the greatest
    common divisor of a and b.

    This function implements the extended Euclidean
    algorithm and runs in O(log b) in the worst case.

    """
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = b, a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def egcd(n, p):
    gcd, x, y = extended_euclidean_algorithm(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        # Either n is 0, or p is not a prime number.
        raise ValueError("{} has no multiplicative inverse " "modulo {}".format(n, p))
    else:
        return x % p


def bits(n):
    while n:
        yield n & 1
        n >>= 1


def multiply(a, b, m, w):
    ans = T(0, 0)
    ans.p = (a.p * b.p % m + a.d * b.d % m * w % m) % m
    ans.d = (a.p * b.d % m + a.d * b.p % m) % m
    return ans


def power(a, b, m, w):
    ans = T(1, 0)
    while b:
        if b & 1:
            ans = multiply(ans, a, m, w)
            b -= 1
        b = b >> 1
        a = multiply(a, a, m, w)
    return ans


def pow_mod(a, b, c):
    a = a % c
    ans = 1
    while b != 0:
        if b & 1:
            ans = (ans * a) % c
        b >>= 1
        a = (a * a) % c
    return ans


def positive_mod(a, m):
    a %= m
    if a < 0:
        a += m
    return a


def cipolla_alg(n, p):
    if p == 2:
        return 1
    if pow_mod(n, (p - 1) >> 1, p) + 1 == p:
        return -1
    while 1:
        a = random.randint(0, p + 1)
        t = a * a - n
        w = positive_mod(t, p)
        if pow_mod(w, (p - 1) >> 1, p) + 1 == p:
            break
    tmp = T(a, 1)
    ans = power(tmp, (p + 1) >> 1, p, w)
    return min(p - ans.p, ans.p)
