"""
Exotic* Curves - solve script

Vulnerability:
    The "point addition" in chall.py isn't real elliptic curve addition:

        Rx = Px*Qx + D*Py*Qy  (mod p)
        Ry = Px*Qy + Py*Qx    (mod p)

    That's exactly multiplication in the ring Z_p[sqrt(D)] -- i.e. treating
    each "point" (x, y) as the element x + y*sqrt(D). "Points" are really
    just elements of a quadratic extension of F_p, and "scalar_mul" is
    just exponentiation in that ring.

    D turns out to be a quadratic non-residue mod p, so the ring is a
    field isomorphic to F_(p^2), and every public "point" here (G, A, B)
    has norm 1 -- meaning they all live inside the cyclic subgroup of
    order p+1, NOT the full order p^2-1.

    p+1 factors almost entirely into small primes (nothing bigger than a
    59-bit prime), so the discrete log of Bob's private key is directly
    solvable with Pohlig-Hellman (BSGS for the small factors, Pollard's
    rho for the 59-bit one). Once we recover n_b, we compute the real
    shared secret A^n_b, derive the AES key exactly like the challenge
    does, and decrypt the flag.
"""

import math
import random

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from hashlib import sha1

# ---- challenge parameters (from output(EXOTIC).txt) ----
p = 106267532015697168520337191172088148412515620576161290874946589402878151571249
D = 42233242539448005099475028269993990446352013294366498148311505626717263001612

# G is a fixed constant baked into chall.py (not printed in the output)
G = (102048330668061011078177084521527399007542737797660957136363503399801919446230,
     73159115351277642048716110709055707500362539496317081461959122153668971225415)

A = (13576866167002229829628682212089073935524598703068420926007376235818728075607,
     24596311476190289480258356776256149104553730312606239661463353580061167337137)
B = (25969029228340787796927547951552192885641602829554221315818875377640814404070,
     55051918571465903426055630502090765909144252223579472291416558946996065912443)

IV = bytes.fromhex("90ebd72eb142152246c7ed29d09d7f4f")
CT = bytes.fromhex("4ca3655a9d842a47cc9db587dbcdb36c6f822acd1f2c84ede72473d81b7b6c6"
                    "bbdcd2b12a7a1999b9c10bb44b4d78153")

IDENTITY = (1, 0)


# ---- "point" arithmetic == multiplication in Z_p[sqrt(D)] ----
def mul(P, Q):
    return ((P[0] * Q[0] + D * P[1] * Q[1]) % p,
            (P[0] * Q[1] + P[1] * Q[0]) % p)


def inv(P):
    # norm(P) = 1 for everything in our subgroup, so the inverse of
    # x + y*sqrt(D) is just its conjugate x - y*sqrt(D)
    return (P[0], (-P[1]) % p)


def power(P, n):
    R = IDENTITY
    while n > 0:
        if n & 1:
            R = mul(R, P)
        P = mul(P, P)
        n >>= 1
    return R


def norm(P):
    return (P[0] * P[0] - D * P[1] * P[1]) % p


# ---- Pohlig-Hellman machinery ----
def bsgs(g, h, n):
    """Solve g^x = h for x in [0, n)."""
    m = math.isqrt(n) + 1
    table = {}
    e = IDENTITY
    for j in range(m):
        table[e] = j
        e = mul(e, g)
    g_m_inv = inv(power(g, m))
    gamma = h
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = mul(gamma, g_m_inv)
    raise ValueError("no discrete log found")


def pollard_rho_dlp(g, h, n):
    """Solve g^x = h for x in [0, n), for larger n via Pollard's rho."""
    while True:
        a, b = random.randrange(n), random.randrange(n)
        X = mul(power(g, a), power(h, b))
        a2, b2, X2 = a, b, X

        def step(X, a, b):
            branch = X[0] % 3
            if branch == 0:
                return mul(X, g), (a + 1) % n, b
            elif branch == 1:
                return mul(X, h), a, (b + 1) % n
            else:
                return mul(X, X), (2 * a) % n, (2 * b) % n

        for _ in range(20_000_000):
            X, a, b = step(X, a, b)
            X2, a2, b2 = step(*step(X2, a2, b2))
            if X == X2:
                break
        else:
            continue

        r = (b - b2) % n
        if r == 0:
            continue
        try:
            x = (pow(r, -1, n) * (a2 - a)) % n
        except ValueError:
            continue
        if power(g, x) == h:
            return x


def discrete_log(base, target, order, factors):
    """Pohlig-Hellman: recover x (mod order-of-base) with base^x = target."""
    residues, moduli = [], []
    for q, e in factors.items():
        n = q ** e
        cofactor = order // n
        g_i = power(base, cofactor)
        h_i = power(target, cofactor)
        if g_i == IDENTITY:
            continue  # base's order doesn't include this factor
        xi = bsgs(g_i, h_i, n) if n < 2_000_000 else pollard_rho_dlp(g_i, h_i, n)
        residues.append(xi)
        moduli.append(n)

    x, mod = residues[0], moduli[0]
    for xi, ni in zip(residues[1:], moduli[1:]):
        # CRT combine (mod, ni) pair by pair
        g_ = math.gcd(mod, ni)
        assert g_ == 1, "unexpected shared factor in CRT combine"
        x = (x * ni * pow(ni, -1, mod) + xi * mod * pow(mod, -1, ni)) % (mod * ni)
        mod *= ni
    return x, mod


def solve():
    # p+1 is smooth, exactly the structure Pohlig-Hellman needs.
    M = p + 1
    factors = {
        2: 1, 3: 7, 5: 4, 7: 3, 11: 6, 13: 3, 17: 1, 19: 4, 23: 2, 29: 4,
        31: 2, 41: 1, 257: 1, 468274927: 1, 13540745363: 1,
        547099953729365581: 1,
    }
    assert math.prod(q ** e for q, e in factors.items()) == M
    assert norm(G) == norm(A) == norm(B) == 1  # confirms the norm-1 subgroup

    n_b, order = discrete_log(G, B, M, factors)
    assert power(G, n_b) == B

    shared = power(A, n_b)
    key = sha1(str(shared[0]).encode()).digest()[:16]

    cipher = Cipher(algorithms.AES(key), modes.CBC(IV))
    dec = cipher.decryptor()
    pt = dec.update(CT) + dec.finalize()
    return pt


if __name__ == "__main__":
    flag = solve()
    print(flag)