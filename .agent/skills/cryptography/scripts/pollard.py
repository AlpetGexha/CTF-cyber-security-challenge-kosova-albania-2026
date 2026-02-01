
import math

# From n.txt
n_str = "137469256394066944221704319829565625989159757972874615636971657187608792473122683161091642028881297663640805874479009822709847389498103114938809682187186891057234584696781099075605264455876133037400383349712960678153810236527870081072760713929693128936222668700205860778624902601792052418650261924881126024917"
n = int(n_str)

def pollard_pm1(n, B=100000):
    a = 2
    for p in range(2, B+1):
        a = pow(a, p, n)
        d = math.gcd(a - 1, n)
        if 1 < d < n:
            return d
    return None

print("Running Pollard's p-1...")
p = pollard_pm1(n, 1000000) # Increased Bound
if p:
    print(f"Found factor p = {p}")
    print(f"q = {n // p}")
else:
    print("Pollard's p-1 failed.")
