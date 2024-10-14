import numpy as np
from matplotlib import pyplot as plt
from calculate_tools import egcd, bits, pow_mod, positive_mod, cipolla_alg


class EllipticCurve:
    def __init__(self, a, b, p, GF=None):
        if 4 * a**3 + 27 * b**2 == 0:
            raise ValueError("Curve contains singularities")
        self.a = a
        self.b = b
        self.p = p
        self.x = []
        self.y_positive = np.array([], dtype="int32")
        self.y_negative = np.array([], dtype="int32")
        self.points = []
        self.GF = GF
        self.know_GF = GF is not None

    def get_GF(self, GF):
        self.GF = GF
        self.know_GF = True

    def __gen_x_y(self):
        # Generate points (x, y) on the curve.
        y_values = []
        for x in range(0, self.p):
            y_squared = pow(x, 3) + x * self.a + self.b
            if pow_mod(y_squared, (self.p - 1) // 2, self.p) == 1:
                y_values.append(cipolla_alg(y_squared, self.p))
                self.x.append(x)
            elif y_squared % self.p == 0:
                self.x.append(x)
                y_values.append(0)

        self.y_positive = np.array(y_values, dtype="int32")
        self.y_negative = self.p - self.y_positive
        self.x = np.array(self.x, dtype="int32")

        for x, y_pos in zip(self.x, self.y_positive):
            self.points.append((x, y_pos))
            self.points.append((x, self.p - y_pos))

    def is_on_curve(self, point):
        # Check if the point is on the curve
        x, y = point
        return (x**3 + self.a * x + self.b - y**2) % self.p == 0

    def scalar_mult(self, n, P):
        # Compute n*P using double-and-add algorithm
        assert self.is_on_curve(P)
        if n == 0:
            return (0, 0)
        if n < 0:
            return self.scalar_mult(-n, (P[0], -P[1] % self.p))

        if self.know_GF:
            n %= self.GF

        R = (0, 0)
        for bit in bits(n):
            if bit:
                R = self.add_points(P, R)
            P = self.add_points(P, P)
        return R

    def add_points(self, P, Q):
        # Add two points P and Q
        if P == (0, 0):
            return Q
        if Q == (0, 0):
            return P

        if P == Q:
            inv = egcd(2 * P[1], self.p)
            slope = (3 * P[0] ** 2 + self.a) * inv % self.p
        else:
            inv = egcd(P[0] - Q[0], self.p)
            slope = (P[1] - Q[1]) * inv % self.p

        x_r = (slope**2 - P[0] - Q[0]) % self.p
        y_r = (slope * (P[0] - x_r) - P[1]) % self.p
        return positive_mod(x_r, self.p), positive_mod(y_r, self.p)

    def __str__(self):
        return f"$$ y^2 ≡ x^3 + {self.a}x + {self.b} (mod {self.p}) $$"
