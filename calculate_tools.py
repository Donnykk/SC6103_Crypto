import random


def bits(n):
    # Generates the bits of integer n
    while n:
        yield n & 1
        n >>= 1


def pow_mod(a, exp, mod):
    # Standard mod exponentiation
    result = 1
    a = a % mod
    while exp:
        if exp & 1:
            result = (result * a) % mod
        a = (a * a) % mod
        exp >>= 1
    return result


def positive_mod(a, mod):
    # Computes the positive mod
    return (a % mod + mod) % mod


def extended_euclidean_algorithm(a, b):
    # Extended Euclidean Algorithm to find the greatest common divisor
    x, last_x = 0, 1
    y, last_y = 1, 0
    while b != 0:
        quotient = a // b
        a, b = b, a - quotient * b
        last_x, x = x, last_x - quotient * x
        last_y, y = y, last_y - quotient * y
    return a, last_x, last_y


def egcd(n, p):
    # Computes the modular inverse of n modulo p
    gcd, x, _ = extended_euclidean_algorithm(n, p)
    if gcd != 1:
        raise ValueError(f"{n} has no multiplicative inverse modulo {p}")
    return x % p


class T:
    def __init__(self, real, imag):
        self.real = real  # Real part
        self.imag = imag  # Imaginary part


def multiply(a, b, mod, w):
    # Multiplication in Cipolla's algorithm, returning the result of (a * b) mod p
    real = (a.real * b.real + a.imag * b.imag * w) % mod
    imag = (a.real * b.imag + a.imag * b.real) % mod
    return T(real, imag)


def power(a, exp, mod, w):
    # Fast exponentiation (a^exp) mod p using Cipolla's algorithm
    result = T(1, 0)
    while exp:
        if exp & 1:
            result = multiply(result, a, mod, w)
        a = multiply(a, a, mod, w)
        exp >>= 1
    return result


def cipolla_alg(n, p):
    # Cipolla's algorithm to find a square root of n modulo p
    if p == 2:
        return 1
    if pow_mod(n, (p - 1) // 2, p) == p - 1:
        # n is not a quadratic residue, no solution
        return -1
    while True:
        a = random.randint(0, p - 1)
        w = positive_mod(a * a - n, p)
        if pow_mod(w, (p - 1) // 2, p) == p - 1:
            break
    tmp = T(a, 1)
    ans = power(tmp, (p + 1) // 2, p, w)
    return min(p - ans.real, ans.real)
