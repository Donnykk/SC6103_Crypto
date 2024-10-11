def get_points(a, b, p):
    # Generate the points set
    points = []
    for x in range(p):
        y_square = (x**3 + a * x + b) % p
        for y in range(p):
            if (y**2) % p == y_square:
                points.append((x, y))
    return points


def cal_k(point_A, point_B, p):
    # Calculate the slope
    if point_A == point_B:
        son = 3 * pow(point_A[0], 2) + a
        mother = 2 * point_A[1]
        return (son * pow(mother, p - 2, p)) % p
    else:
        son = point_B[1] - point_A[1]
        mother = point_B[0] - point_A[0]
        return (son * pow(mother, p - 2, p)) % p


def cal_add(point_A, point_B, p, k):
    # Calculate adding points
    cx = (k**2 - point_A[0] - point_B[0]) % p
    cy = (k * (point_A[0] - cx) - point_A[1]) % p
    return cx, cy


def cal_NA(key, point_A, point_B, p):
    # Calculate the multiplication
    for i in range(key - 1):
        k = cal_k(point_A, point_B, p)
        point_B = cal_add(point_A, point_B, p, k)
    return point_B


def encryption(r, Q, m, p):
    cx = cal_NA(r, A, B, p)
    rQ = cal_NA(r, Q, Q, p)
    k = cal_k(m, rQ, p)
    cy = cal_add(m, rQ, p, k)
    return cx, cy


def decryption(cplantext, key, p):
    kc2 = cal_NA(key, cplantext[0], cplantext[0], p)
    kc2 = (kc2[0], -kc2[1])
    k = cal_k(cplantext[1], kc2, p)
    result = cal_add(cplantext[1], kc2, p, k)
    return result


# Elliptic curve parameters
a = 1
b = 6
p = 11
key = 7

points = get_points(a, b, p)
print("Elements in the point set:")
print(points, end="")
print("\n-------------------------------------------------------------------")

A = (2, 7)
B = (2, 7)
Q = cal_NA(key, A, B, p)
r = 3
message = (10, 9)

print(f"Original message: {message}")

c = encryption(r, Q, message, p)
print(f"Encrypted result: {c}")
result = decryption(c, key, p)
print(f"Decrypted result: {result}")
