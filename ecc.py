import hashlib


def get_points(a, b, p):
    # Generate the points set
    points = []
    for x in range(p):
        y_square = (x**3 + a * x + b) % p
        for y in range(p):
            if (y**2) % p == y_square:
                points.append((x, y))
                print(x, y)
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
    # Calculate the random point rG
    cx = cal_NA(r, G, G, p)
    rQ = cal_NA(r, Q, Q, p)
    # Calculate the slope between the message point and rQ
    k = cal_k(m, rQ, p)
    cy = cal_add(m, rQ, p, k)
    return cx, cy


def decryption(cplantext, key, p):
    # Calculate kC2
    kc2 = cal_NA(key, cplantext[0], cplantext[0], p)
    # Negate the y coordinate of kc2 and take it mod p
    kc2 = (kc2[0], -kc2[1] % p)
    # Calculate the slope between c1 and -kC2
    k = cal_k(cplantext[1], kc2, p)
    # Add the points c1 and -kC2
    result = cal_add(cplantext[1], kc2, p, k)
    return result


def is_on_curve(x, y, a, b, p):
    return (y**2) % p == (x**3 + a * x + b) % p


def message_to_point(message, a, b, p):
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    message_int = int(message_hash, 16) % p

    # Find a valid y coordinate that satisfies the curve equation
    y_square = (message_int**3 + a * message_int + b) % p
    for y in range(p):
        # print(y, y_square)
        if (y**2) % p == y_square:
            return (message_int, y)

    raise ValueError("No valid point found for this message.")


# secp112r1 Elliptic curve parameters
a = 2
b = 3
p = 101

points = get_points(a, b, p)
print("Elements in the point set:")
print(points, end="")
print("\n-------------------------------------------------------------------")

G = (5, 80)

# private key
key = 7

# public key
Q = cal_NA(key, G, G, p)
r = 15

message = "This is a message"
message_point = message_to_point(message, a, b, p)

print(f"Original message: {message}")
print(f"Message point: {message_point}")
print("-------------------------------")

c = encryption(r, Q, message_point, p)
print(f"Encrypted result: {c}")
print("-------------------------------")

result = decryption(c, key, p)
print(f"Decrypted result: {result}")
