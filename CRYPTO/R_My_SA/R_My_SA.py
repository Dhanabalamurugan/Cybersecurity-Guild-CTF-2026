import math
import random
from sympy import isprime
 
def pollard_rho_brent(n: int) -> int:
    if n % 2 == 0:
        return 2
    while True:
        y = random.randint(1, n - 1)
        c = random.randint(1, n - 1)
        m = random.randint(1, n - 1)
        g = r = q = 1
        x = ys = 0
        while g == 1:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g = math.gcd(q, n)
                k += m
            r *= 2
        if g != n:
            return g
 
 
def fully_factor(n: int, factors: list):
    if n == 1:
        return
    if isprime(n):
        factors.append(n)
        return
    f = pollard_rho_brent(n)
    fully_factor(f, factors)
    fully_factor(n // f, factors)
 
 
def solve():
    n = 610870240865234529907743614451858801440155492757079465096710603276200472290332312307451743490652760649679857285194802523705355655732590457358769052210759328095574632949925216971079564253285551079681286819576086292966982023640170817829686489069479455782174911021436314674483460806303999075272232571864598274720703485318203442053573948268875433041811318199331
    e = 65537
    ct = 269502667676232352065057019549198430447003590244768780011937512108750638388052071680107935792375411406856203708540602606052505183332456367255459084740242095067533827164103921553415851493514793496968994176547304138220110710286537331520492430193350534011015869917837578280239839478693713969444834925766299298505300587378553503027879397491554035163970710898956
 
    factors = []
    fully_factor(n, factors)
    assert math.prod(factors) == n
 
    phi = 1
    for p in factors:
        phi *= (p - 1)
 
    d = pow(e, -1, phi)
    m = pow(ct, d, n)
    return m.to_bytes((m.bit_length() + 7) // 8, 'big'), factors
 
 
if __name__ == "__main__":
    flag, factors = solve()
    print(f"recovered {len(factors)} prime factors (~{factors[0].bit_length()} bits each)")
    print(flag)