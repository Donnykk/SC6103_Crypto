from sympy.ntheory import factorint
from sympy.ntheory.modular import crt


# Generate the set of points on the elliptic curve
def get_points(a, b, p):
    points = []
    for x in range(p):
        y_square = (x**3 + a * x + b) % p
        for y in range(p):
            if (y**2) % p == y_square:
                points.append((x, y))
    return points


# Elliptic curve point addition
def point_add(P, Q, p, a):
    if P == Q:
        s = (3 * P[0] ** 2 + a) * pow(2 * P[1], p - 2, p) % p
    else:
        s = (Q[1] - P[1]) * pow(Q[0] - P[0], p - 2, p) % p
    x = (s**2 - P[0] - Q[0]) % p
    y = (s * (P[0] - x) - P[1]) % p
    return (x, y)


# Scalar multiplication of a point on the elliptic curve
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


# Pohlig-Hellman attack main function
def pohlig_hellman(P, Q, p, a, order):
    factors = factorint(order)  # Factor the order
    x_list = []
    mod_list = []

    for q, e in factors.items():
        print(f"Processing prime factor: q = {q}, e = {e}")
        q_exp = q**e
        x_q = 0

        # Solve the sub-problem for each prime factor q
        for j in range(e):
            # Compute P^(order/q^(j+1))
            Q_j = scalar_mult(order // (q ** (j + 1)), Q, p, a)
            P_j = scalar_mult(order // (q ** (j + 1)), P, p, a)

            # Solve the sub-problem via brute-force search
            for x_j in range(q):
                if scalar_mult(x_j, P_j, p, a) == Q_j:
                    x_q += x_j * (q**j)
                    break

        x_list.append(x_q)
        mod_list.append(q_exp)

    # Combine the results using the Chinese Remainder Theorem
    x, _ = crt(mod_list, x_list)
    return x


# Elliptic curve parameters
a = 2
b = 3
p = 101
order = 19  
P = (2, 7)
Q = scalar_mult(7, P, p, a)  

private_key = pohlig_hellman(P, Q, p, a, order)
print(f"Recovered private key: {private_key}")
