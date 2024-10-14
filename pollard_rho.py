from elliptic_curve import EllipticCurve
from calculate_tools import egcd
import random


class PollardRhoSequence:
    def __init__(self, point1, point2, E):
        self.point1 = point1
        self.point2 = point2
        self.E = E

        # Precompute random coefficients and corresponding points
        self.add_a1 = random.randrange(1, E.GF)
        self.add_b1 = random.randrange(1, E.GF)
        self.add_x1 = E.add_points(
            E.scalar_mult(self.add_a1, point1),
            E.scalar_mult(self.add_b1, point2),
        )

        self.add_a2 = random.randrange(1, E.GF)
        self.add_b2 = random.randrange(1, E.GF)
        self.add_x2 = E.add_points(
            E.scalar_mult(self.add_a2, point1),
            E.scalar_mult(self.add_b2, point2),
        )

    def __iter__(self):
        # Partition the elliptic curve's x-coordinates into 3 segments
        partition_size = self.E.p // 3 + 1

        x, a, b = (
            (0, 0),
            0,
            0,
        )

        while True:
            # Determine segment based on x[0]
            i = x[0] // partition_size if x != (0, 0) else 0

            if i == 0:
                # First segment: Update a, b and x using the first precomputed point
                a = (a + self.add_a1) % self.E.GF
                b = (b + self.add_b1) % self.E.GF
                x = self.E.add_points(x, self.add_x1)
            elif i == 1:
                # Second segment: Double x, a, b (scalar multiply by 2)
                a = (a * 2) % self.E.GF
                b = (b * 2) % self.E.GF
                x = self.E.scalar_mult(2, x)
            elif i == 2:
                # Third segment: Update a, b and x using the second precomputed point
                a = (a + self.add_a2) % self.E.GF
                b = (b + self.add_b2) % self.E.GF
                x = self.E.add_points(x, self.add_x2)
            else:
                raise AssertionError(i)

            yield x, a, b


def log(p, q, curve):
    assert curve.is_on_curve(p)
    assert curve.is_on_curve(q)

    # Try Pollard's Rho algorithm at most three times to handle potential failures
    for attempt in range(3):
        sequence = PollardRhoSequence(p, q, curve)

        tortoise, hare = iter(sequence), iter(sequence)

        # Iterate through points in Pollard's Rho sequence
        for j in range(curve.GF):
            # Tortoise moves one step, hare moves two steps
            x1, a1, b1 = next(tortoise)
            x2, a2, b2 = next(hare)
            x2, a2, b2 = next(hare)

            # Check if tortoise and hare are at the same point
            if x1 == x2:
                # Avoid division by zero by retrying with a new random sequence
                if b1 == b2:
                    break
                # Compute the logarithm using the extended Euclidean algorithm
                x = (a1 - a2) * egcd(b2 - b1, curve.GF)
                logarithm = x % curve.GF
                steps = attempt * curve.GF + j + 1
                return logarithm, steps

    raise AssertionError("Pollard's Rho algorithm failed after 3 attempts")


if __name__ == "__main__":
    E = EllipticCurve(a=1, b=-1, p=10177, GF=10331)
    p = (0x1, 0x1)
    q = (0x1A28, 0x8FB)
    result = log(p, q, E)
    # private_key = 325
    print(result)
