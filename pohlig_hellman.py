from sympy.ntheory import factorint
from sympy.ntheory.modular import crt


# Optimized elliptic curve point addition
def point_add(P, Q, p, a):
    if P == Q:
        s = (3 * P[0] ** 2 + a) * pow(2 * P[1], p - 2, p) % p
    else:
        s = (Q[1] - P[1]) * pow(Q[0] - P[0], p - 2, p) % p
    x = (s**2 - P[0] - Q[0]) % p
    y = (s * (P[0] - x) - P[1]) % p
    return (x, y)


# Optimized scalar multiplication using double-and-add algorithm
def scalar_mult(k, P, p, a):
    R = None
    while k > 0:
        if k % 2 == 1:
            if R is None:
                R = P
            else:
                R = point_add(R, P, p, a)
        P = point_add(P, P, p, a)
        k //= 2
    return R


# Pohlig-Hellman attack for large primes (64-bit key size)
def pohlig_hellman(P, Q, p, a, order):
    # Factorize the group order
    factors = factorint(order)
    x_list = []
    mod_list = []

    for q, e in factors.items():
        q_exp = q**e  # q^e
        x_q = 0

        for j in range(e):
            # Compute P^(order / q^(j+1)) and Q^(order / q^(j+1))
            Q_j = scalar_mult(order // (q ** (j + 1)), Q, p, a)
            P_j = scalar_mult(order // (q ** (j + 1)), P, p, a)

            # Use brute-force search or optimized algorithms like Baby-step Giant-step
            for x_j in range(q):
                if scalar_mult(x_j, P_j, p, a) == Q_j:
                    x_q += x_j * (q**j)
                    break

        x_list.append(x_q)
        mod_list.append(q_exp)

    # Combine results using Chinese Remainder Theorem
    x, _ = crt(mod_list, x_list)
    return x


# Example: 64-bit elliptic curve parameters
a = 2
b = 3
p = 9223372036854775783
order = 9223372036854775737
P = (5, 80)
# public key
Q = scalar_mult(1000, P, p, a)
print(Q)

private_key = pohlig_hellman(P, Q, p, a, order)
print(f"Recovered private key: {private_key}")
