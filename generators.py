# Vasiliu Ana - IIA3

import random
import time
import math
from Cryptodome.Util import number


def test_output(output):
    print("Procentaj de 0: " + str(output.count("0") / len(output) * 100))
    print("Procentaj de 1: " + str(output.count("1") / len(output) * 100))


def blum_blum_generator():
    p = number.getPrime(512)
    while p % 4 != 3:
        p = number.getPrime(512)
    q = number.getPrime(512)
    while q % 4 != 3:
        q = number.getPrime(512)

    n = p * q
    l = pow(2, 10)
    s = int(time.time())
    x = [pow(s, 2) % n]
    output = chr(x[0] % 2 + ord("0"))
    for i in range(1, l):
        x.append(pow(x[i - 1], 2) % n)
        output += chr(x[i] % 2 + ord("0"))
    return output


start_time = time.time()
bb_output = blum_blum_generator()
elapsed_time = time.time() - start_time

print("Timp de executie pentru generatorul Blum-Blum: ")
print("%s secunde" % elapsed_time)

print("Rezultat generator Blum-Blum: ")
print(bb_output)
test_output(bb_output)


def jacobi(n, k):
    n %= k
    result = 1
    while n != 0:
        while n % 2 == 0:
            n /= 2
            if (k % 8) in (3, 5):
                result = -result
        n, k = k, n
        if n % 4 == 3 and k % 4 == 3:
            result = -result
        n %= k
    if k == 1:
        return result
    else:
        return 0


def jacobi_generator():
    false_pos_prob = 0.000000000000000000000001
    p = number.getPrime(512)
    while not (number.isPrime(p, false_pos_prob)) or p % 4 != 3:
        p = number.getPrime(512)
    q = number.getPrime(512)
    while not (number.isPrime(q, false_pos_prob)) or q % 4 != 3:
        q = number.getPrime(512)
    n = p * q
    l = pow(2, 10)
    a = int(time.time() * 1000)
    while math.gcd(a, n) != 1:
        a = int(time.time())
    output = ""
    for i in range(1, l):
        jacobi_symbol = jacobi(a + i, n)
        if jacobi_symbol == 0:
            return "error"
        if jacobi_symbol == -1:
            jacobi_symbol = 0
        output += chr(jacobi_symbol + ord("0"))
    return output


start_time = time.time()
jacobi_output = jacobi_generator()
while jacobi_output == "error":
    jacobi_output = jacobi_generator()
elapsed_time = time.time() - start_time

print("\nTimp de executie pentru generatorul Jacobi: ")
print("%s secunde" % elapsed_time)

print("Rezultat generator Jacobi: ")
print(jacobi_output)
test_output(jacobi_output)


def lfsr():
    l = 10
    pol = [10, 3]
    pos = []
    for i in range(0, len(pol)):
        pos.append(l - pol[i])

    d = random.getrandbits(l)
    t = pow(2, l) - 1
    output = [d & 1]
    for i in range(0, t):
        a = (d >> pos[0]) & 1
        b = (d >> pos[1]) & 1
        res = a ^ b
        d = d >> 1
        mask = 1 << (l - 1)
        d = d & ~mask
        if res == 1:
            d = d | (1 << (l - 1))
        output.append(d & 1)
    return output


start_time = time.time()
lfsr_output = lfsr()
elapsed_time = time.time() - start_time

print("\nTimp de executie pentru generatorul LFSR: ")
print("%s secunde" % elapsed_time)

print("Rezultat generator LFSR: ")
print(lfsr_output)
