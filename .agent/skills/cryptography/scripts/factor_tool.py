
import math

# From n.txt
n_str = "137469256394066944221704319829565625989159757972874615636971657187608792473122683161091642028881297663640805874479009822709847389498103114938809682187186891057234584696781099075605264455876133037400383349712960678153810236527870081072760713929693128936222668700205860778624902601792052418650261924881126024917"
n = int(n_str)
print(f"N = {n}")

def isqrt(n):
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def fermat_factor(n):
    a = isqrt(n)
    if a * a < n:
        a += 1
    count = 0
    while True:
        if count % 1000000 == 0:
            print(f"Fermat iteration {count}...")
        
        b2 = a * a - n
        if b2 >= 0:
            b = isqrt(b2)
            if b * b == b2:
                return (a - b, a + b)
        a += 1
        count += 1
        if count > 5000000: # Give up after 5M iterations
            return None

print("Checking fermat...")
res = fermat_factor(n)
if res:
    p, q = res
    print(f"Found factors!\nP = {p}\nQ = {q}")
else:
    print("Fermat failed.")

# Check for perfect power
# n = x^k
# check k=2, 3...
for k in range(2, 10):
    root = int(n ** (1/k))
    if root ** k == n:
        print(f"Found perfect power! N = {root}^{k}")
    if (root + 1) ** k == n:
        print(f"Found perfect power! N = {root+1}^{k}")

