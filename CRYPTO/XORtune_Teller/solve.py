"""
XORtune Teller - solve script

Vulnerability:
    The challenge encrypts each 4-byte block with rng.state *before*
    calling next() (i.e. block i is XORed with state s_i, then next()
    advances to s_{i+1}). After encrypting, it leaks the low byte of
    5 consecutive *future* states (s_12..s_16, since ciphertext has
    12 blocks). That's 40 linear equations in the 32 unknown bits of
    s_12 -> solvable via Gaussian elimination over GF(2).

    Once s_12 is recovered, walk backwards with L^-1 twelve times to
    recover the original keystream s_0..s_11 used to encrypt, then
    XOR-decrypt the ciphertext.
"""

MASK = 0xFFFFFFFF


def next_state(x: int) -> int:
    x &= MASK
    x ^= (x << 13) & MASK
    x ^= (x >> 17)
    x ^= (x << 5) & MASK
    return x & MASK

def build_matrix():
    L = [[0] * 32 for _ in range(32)]
    for i in range(32):
        ns = next_state(1 << i)
        for j in range(32):
            L[j][i] = (ns >> j) & 1
    return L

def int_to_bits(x):
    return [(x >> i) & 1 for i in range(32)]


def bits_to_int(b):
    x = 0
    for i in range(32):
        x |= b[i] << i
    return x


def matvec(M, v):
    res = [0] * 32
    for j in range(32):
        s = 0
        row = M[j]
        for i in range(32):
            if row[i] and v[i]:
                s ^= 1
        res[j] = s
    return res


def matmul(A, B):
    C = [[0] * 32 for _ in range(32)]
    for i in range(32):
        for k in range(32):
            if A[i][k]:
                rowB, rowC = B[k], C[i]
                for j in range(32):
                    if rowB[j]:
                        rowC[j] ^= 1
    return C


def invert_matrix(M):
    n = 32
    aug = [M[i][:] + [1 if i == j else 0 for j in range(n)] for i in range(n)]
    row = 0
    for col in range(n):
        sel = next((r for r in range(row, n) if aug[r][col]), None)
        if sel is None:
            raise ValueError("singular matrix")
        aug[row], aug[sel] = aug[sel], aug[row]
        for r in range(n):
            if r != row and aug[r][col]:
                aug[r] = [aug[r][c] ^ aug[row][c] for c in range(2 * n)]
        row += 1
    return [r[n:] for r in aug]


def gf2_solve(equations, rhs, nvars=32):
    """Gaussian elimination over GF(2). Returns solution bit vector."""
    A = [row[:] + [rhs[i]] for i, row in enumerate(equations)]
    nrows, ncols = len(A), nvars + 1
    pivots, row = {}, 0
    for col in range(nvars):
        sel = next((r for r in range(row, nrows) if A[r][col]), None)
        if sel is None:
            continue
        A[row], A[sel] = A[sel], A[row]
        for r in range(nrows):
            if r != row and A[r][col]:
                A[r] = [A[r][c] ^ A[row][c] for c in range(ncols)]
        pivots[col] = row
        row += 1
    sol = [0] * nvars
    for col, r in pivots.items():
        sol[col] = A[r][nvars]
    return sol


def solve():
    ct = (b'\x8e\xad\xa0"\x052E\xd4\x9bQr\xd3*\xf6Y\xfb\x01TB\xdejd_J\xa9\xe4'
          b'\xbc\xf7Dq\x04\r \x12k\xc9%,J\x00m\x9dS\xc9e\xc7#\x98')
    leaked_low_bytes = [130, 101, 250, 179, 100]  # low byte of s_12..s_16

    L = build_matrix()
    Linv = invert_matrix(L)

    # powers of L: L^0 .. L^4
    I = [[1 if i == j else 0 for i in range(32)] for j in range(32)]
    powers, cur = [I], I
    for _ in range(4):
        cur = matmul(L, cur)
        powers.append(cur)

    # 40 linear equations (8 bits x 5 leaked states) in the 32 bits of s_12
    equations, rhs = [], []
    for k, val in enumerate(leaked_low_bytes):
        for bit in range(8):
            equations.append(powers[k][bit])
            rhs.append((val >> bit) & 1)

    s12 = bits_to_int(gf2_solve(equations, rhs))

    chk = s12
    for val in leaked_low_bytes:
        assert (chk & 0xFF) == val
        chk = next_state(chk)

    # walk backwards 12 steps: s12 -> s11 -> ... -> s0
    state = s12
    states_desc = [state]
    for _ in range(12):
        state = bits_to_int(matvec(Linv, int_to_bits(state)))
        states_desc.append(state)
    keys = list(reversed(states_desc[1:]))  

    pt = b''
    for i, key in enumerate(keys):
        key_bytes = key.to_bytes(4, 'big')
        block = ct[i * 4:(i + 1) * 4]
        pt += bytes(a ^ b for a, b in zip(block, key_bytes))

    return pt


if __name__ == "__main__":
    flag = solve()
    print(flag)