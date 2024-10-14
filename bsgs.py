from elliptic_curve import EllipticCurve
import math


def BSGS(E, p, q):
    """
    Baby-step Giant-step algorithm for solving the discrete logarithm problem on an elliptic curve.

    This algorithm solves for k such that q = k * p, where q and p are points on the elliptic curve E.

    Parameters:
    E -- an instance of the EllipticCurve class
    p -- the elliptic curve point for which the logarithm is to be found
    q -- the result point after scalar multiplication

    Returns:
    (k, steps) -- the scalar k and the number of steps taken to find k
    """
    step = 0
    hash_table = {}
    # Use integer square root for efficiency
    m = math.isqrt(E.GF)
    # Baby step: Precompute multiples of p
    for i in range(m):
        tmp = E.scalar_mult(i, p)
        hash_table[tmp] = i
    # Giant step: Search for matches with q
    for a in range(m):
        amP = E.scalar_mult(-a * m, p)
        Q_amP = E.add_points(amP, q)
        if Q_amP in hash_table:
            return hash_table[Q_amP] + a * m, step
        step += 1
    return None, step


if __name__ == "__main__":
    E = EllipticCurve(a=1, b=-1, p=10177, GF=10331)
    p = (0x1, 0x1)
    q = (0x1A28, 0x8FB)
    result = BSGS(E, p, q)
    # private_key = 325
    print(result)
