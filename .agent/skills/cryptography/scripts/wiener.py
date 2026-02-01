
import sys

# From n.txt
n_str = "137469256394066944221704319829565625989159757972874615636971657187608792473122683161091642028881297663640805874479009822709847389498103114938809682187186891057234584696781099075605264455876133037400383349712960678153810236527870081072760713929693128936222668700205860778624902601792052418650261924881126024917"
n = int(n_str)
e = 65537

sys.setrecursionlimit(2000)

def continued_fractions(n, d):
    output = []
    while d:
        q = n // d
        output.append(q)
        n, d = d, n % d
    return output

def convergents(cf):
    n1, d1 = 1, 0
    n2, d2 = cf[0], 1
    yield n2, d2
    for i in range(1, len(cf)):
        n3, d3 = cf[i] * n2 + n1, cf[i] * d2 + d1
        yield n3, d3
        n1, d1 = n2, d2
        n2, d2 = n3, d3

def is_quadratic_residue(a, p):
    # Euler's criterion
    return pow(a, (p - 1) // 2, p) == 1

def solve_quadratic(a, b, c):
    delta = b*b - 4*a*c
    if delta < 0: return None
    isqrt_delta = int(math.isqrt(delta))
    if isqrt_delta * isqrt_delta != delta: return None
    return (-b + isqrt_delta) // (2*a), (-b - isqrt_delta) // (2*a)

import math

def wiener_attack(e, n):
    print("Generating continued fractions...")
    cf = continued_fractions(e, n)
    print("Checking convergents...")
    for k, d in convergents(cf):
        if k == 0: continue
        if (e * d - 1) % k != 0: continue
        
        phi = (e * d - 1) // k
        
        # x^2 - ((n - phi) + 1)x + n = 0
        # Roots are p, q
        b = -(n - phi + 1)
        res = solve_quadratic(1, b, n)
        if res:
            p, q = res
            if p * q == n:
                return d, p, q
    return None

print("Checking Wiener's attack...")
res = wiener_attack(e, n)
if res:
    d, p, q = res
    print(f"Found private key d via Wiener!\nd = {d}")
else:
    print("Wiener failed.")
